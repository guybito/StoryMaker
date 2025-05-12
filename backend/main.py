from fastapi import FastAPI, HTTPException
from backend.literary_evaluation_engine import (generate_claude_evaluation_report)
from backend.schemas import EvaluationRecord

app = FastAPI()

@app.post("/evaluate", response_model=EvaluationRecord)
async def evaluate_with_provider(
    story_id: int,
    story_title: str,
    story_text: str
):
    try:
        return generate_claude_evaluation_report(story_id, story_title, story_text)
    except ValueError as ve:
        raise HTTPException(status_code=502, detail=f"Claude error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
