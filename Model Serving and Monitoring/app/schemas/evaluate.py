from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class EvaluationResponse(BaseModel):
    status: str
    message: str

class Evaluation(BaseModel):
    timestamp: datetime
    style_name: str
    feedback: Dict
    user_id: Optional[str] = None
    drift_score: Optional[float] = None

class EvaluationList(BaseModel):
    evaluations: List[Evaluation] 