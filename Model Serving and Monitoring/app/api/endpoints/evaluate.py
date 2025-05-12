from fastapi import APIRouter, HTTPException, Form
from typing import Dict, Optional, List
import json
import logging
from ...model_serving import ModelServer
from ...schemas.evaluate import EvaluationResponse, EvaluationList
from ...main import model_server

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_transformation(
    evaluation: str = Form(...),
    style: str = Form(...),
    user_id: Optional[str] = Form(None)
):
    """Collect user feedback on transformed image"""
    try:
        # Parse evaluation JSON string
        try:
            evaluation_dict = json.loads(evaluation)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=422,
                detail="Invalid evaluation format. Must be a valid JSON object."
            )
        
        # Store feedback
        success = await model_server.collect_feedback(
            original_image=None,  # We don't store original images
            transformed_image=None,  # We don't store transformed images
            style_name=style,
            feedback=evaluation_dict,
            user_id=user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to store evaluation"
            )
        
        return EvaluationResponse(
            status="success",
            message="Evaluation recorded successfully"
        )
        
    except Exception as e:
        logger.error(f"Evaluation endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/evaluations", response_model=EvaluationList)
async def get_evaluations():
    """Get recent evaluations"""
    try:
        # Get evaluations from MinIO
        evaluations = model_server.get_recent_evaluations()
        return EvaluationList(evaluations=evaluations)
    except Exception as e:
        logger.error(f"Get evaluations error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 