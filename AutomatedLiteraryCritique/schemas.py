from pydantic import BaseModel
from typing import Any


class EvaluationRecord(BaseModel):
    story_id: int
    story_title: str
    final_score: float
    full_response: Any
