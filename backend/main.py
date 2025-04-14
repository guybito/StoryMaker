from fastapi import FastAPI, HTTPException
from literary_evaluation_engine import (
    generate_openai_evaluation_report,
    generate_claude_evaluation_report,
    generate_gemini_evaluation_report
)
from schemas import EvaluationRecord

app = FastAPI()

@app.post("/evaluate/{provider}", response_model=EvaluationRecord)
async def evaluate_with_provider(
    provider: str,
    story_id: int,
    story_title: str,
    story_text: str
):
    if provider == "openai":
        return await generate_openai_evaluation_report(story_id, story_title, story_text)
    elif provider == "claude":
        return await generate_claude_evaluation_report(story_id, story_title, story_text)
    elif provider == "gemini":
        return await generate_gemini_evaluation_report(story_id, story_title, story_text)
    else:
        raise HTTPException(status_code=400, detail="Unknown provider. Choose from: openai, claude, gemini")
