from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Evaluation(BaseModel):
    style_accuracy: int = Field(
        ...,
        ge=0,
        le=10,
        description="Rating of how well the style was applied (0-10)"
    )
    content_preservation: int = Field(
        ...,
        ge=0,
        le=10,
        description="Rating of how well the original content was preserved (0-10)"
    )
    overall_quality: int = Field(
        ...,
        ge=0,
        le=10,
        description="Overall quality rating of the transformation (0-10)"
    )
    comment: Optional[str] = Field(None, description="Optional feedback comment")

class EvaluationResponse(BaseModel):
    message: str = Field(..., description="Response message")
    evaluation: Dict[str, Any] = Field(..., description="Evaluation record")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the evaluation") 