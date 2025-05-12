from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransformRequest(BaseModel):
    style: str = Field(..., description="Style to apply to the image")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class TransformResponse(BaseModel):
    message: str = Field(..., description="Response message")
    inference_time: float = Field(..., description="Time taken for inference in seconds")
    style_used: str = Field(..., description="Style that was applied")
    drift_score: Optional[float] = Field(None, description="Data drift score if available")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the transformation") 