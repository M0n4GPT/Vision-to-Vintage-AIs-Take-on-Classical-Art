from pydantic import BaseModel
from typing import Dict, Any, Optional

class TransformResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any]

class EvaluationResponse(BaseModel):
    status: str
    message: str
    score: float
    details: Optional[Dict[str, Any]] = None 