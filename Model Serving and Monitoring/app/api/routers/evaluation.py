from fastapi import APIRouter, HTTPException, Form
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import logging
from ...schemas.evaluation import Evaluation, EvaluationResponse
from ...monitoring.metrics import evaluation_metrics
import mlflow
from datetime import datetime
import json
import os

from ...model_serving import ModelServer
from ...core.config import settings

router = APIRouter(prefix="/evaluation", tags=["evaluation"])
logger = logging.getLogger(__name__)

EVALUATIONS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'evaluations.json')

# Pydantic models for evaluation
class Evaluation(BaseModel):
    model_config = {
        'protected_namespaces': (),
        'json_schema_extra': {
            'example': {
                'style_accuracy': 8,
                'content_preservation': 7,
                'overall_quality': 8,
                'comment': 'Great style transfer!'
            }
        }
    }
    style_accuracy: int = Field(ge=0, le=10)
    content_preservation: int = Field(ge=0, le=10)
    overall_quality: int = Field(ge=0, le=10)
    comment: Optional[str] = None

@router.post("/", response_model=EvaluationResponse)
async def submit_evaluation(
    evaluation: Evaluation,
    style: str = Form(...),
    user_id: Optional[str] = Form(None)
):
    """
    Submit an evaluation for a transformed image.
    Includes monitoring for feedback quality and model performance.
    """
    try:
        # Create evaluation record
        eval_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "style": style,
            "user_id": user_id,
            **evaluation.dict()
        }
        
        # Save evaluation
        os.makedirs(os.path.dirname(EVALUATIONS_FILE), exist_ok=True)
        evaluations = []
        if os.path.exists(EVALUATIONS_FILE):
            with open(EVALUATIONS_FILE, 'r') as f:
                evaluations = json.load(f)
        evaluations.append(eval_record)
        with open(EVALUATIONS_FILE, 'w') as f:
            json.dump(evaluations, f, indent=2)
        
        # Update metrics
        evaluation_metrics.total_evaluations.inc()
        evaluation_metrics.style_accuracy.observe(evaluation.style_accuracy)
        evaluation_metrics.content_preservation.observe(evaluation.content_preservation)
        evaluation_metrics.overall_quality.observe(evaluation.overall_quality)
        
        # Log to MLflow
        try:
            mlflow.log_metrics({
                "style_accuracy": evaluation.style_accuracy,
                "content_preservation": evaluation.content_preservation,
                "overall_quality": evaluation.overall_quality
            })
            mlflow.log_param("style", style)
            if user_id:
                mlflow.log_param("user_id", user_id)
        except Exception as e:
            logger.warning(f"Failed to log to MLflow: {str(e)}")
        
        return EvaluationResponse(
            message="Evaluation submitted successfully",
            evaluation=eval_record
        )
        
    except Exception as e:
        evaluation_metrics.errors_total.inc()
        logger.error(f"Error in submit_evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to submit evaluation",
                "message": str(e)
            }
        )

@router.get("/", response_model=List[EvaluationResponse])
async def get_evaluations(
    skip: int = 0,
    limit: int = 10,
    style: Optional[str] = None
):
    """
    Get evaluation history with optional filtering.
    """
    try:
        if not os.path.exists(EVALUATIONS_FILE):
            return []
            
        with open(EVALUATIONS_FILE, 'r') as f:
            evaluations = json.load(f)
        
        # Apply filters
        if style:
            evaluations = [e for e in evaluations if e["style"] == style]
        
        # Apply pagination
        evaluations = evaluations[skip:skip + limit]
        
        return [
            EvaluationResponse(
                message="Evaluation retrieved successfully",
                evaluation=eval_record
            )
            for eval_record in evaluations
        ]
        
    except Exception as e:
        logger.error(f"Error in get_evaluations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve evaluations",
                "message": str(e)
            }
        )

@router.post("/feedback")
async def submit_feedback(
    evaluation: Evaluation,
    style: str = Form(...),
    user_id: Optional[str] = Form(None)
):
    """Submit evaluation feedback for a transformation"""
    try:
        # Store feedback
        feedback = {
            "style_accuracy": evaluation.style_accuracy,
            "content_preservation": evaluation.content_preservation,
            "overall_quality": evaluation.overall_quality,
            "comment": evaluation.comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        success = await model_server.collect_feedback(style, feedback, user_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Feedback storage failed",
                    "message": "Failed to store your feedback",
                    "suggestion": "Please try again later",
                    "details": "Failed to store feedback in MinIO"
                }
            )

        # Log metrics
        try:
            mlflow.log_metric("style_accuracy", evaluation.style_accuracy)
            mlflow.log_metric("content_preservation", evaluation.content_preservation)
            mlflow.log_metric("overall_quality", evaluation.overall_quality)
        except Exception as e:
            logger.warning(f"Failed to log evaluation metrics: {str(e)}")
        
        return {"message": "Feedback received successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in feedback endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "suggestion": "Please try again later",
                "details": str(e)
            }
        )

@router.get("/feedback")
async def get_feedback(
    skip: int = 0,
    limit: int = 10,
    style: Optional[str] = None
):
    """Get recent feedback with pagination"""
    try:
        # Validate pagination parameters
        if skip < 0 or limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid pagination parameters",
                    "message": "Invalid skip or limit values",
                    "suggestion": "Use skip >= 0 and 1 <= limit <= 100",
                    "details": f"skip={skip}, limit={limit}"
                }
            )
        
        # Get feedback
        feedback = model_server.get_recent_evaluations(limit=limit)
        
        # Filter by style if specified
        if style:
            feedback = [f for f in feedback if f.get("style_name") == style]
        
        # Apply pagination
        total = len(feedback)
        feedback = feedback[skip:skip + limit]
        
        return {
            "feedback": feedback,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in feedback retrieval: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "suggestion": "Please try again later",
                "details": str(e)
            }
        ) 