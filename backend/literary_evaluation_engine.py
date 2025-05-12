import openai
import anthropic
# import google.generativeai as genai
import os
import httpx
import json
from backend.schemas import EvaluationRecord
from pathlib import Path



anthropic_client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")


BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "evaluation_prompt.txt", "r", encoding="utf-8") as f:
    CRITERIA_PROMPT = f.read()

async def generate_claude_evaluation_report(story_id: int, story_title: str, story_text: str) -> EvaluationRecord:
    prompt = CRITERIA_PROMPT.format(story=story_text, title=story_title, id=story_id)
    response = await anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    if not response or not response.content or not response.content[0].text.strip():
        raise ValueError("Empty or invalid response from Claude.")

    content = response.content[0].text
    return _parse_response(story_id, story_title, content)


def _parse_response(story_id: int, story_title: str, content: str) -> EvaluationRecord:
    lines = content.splitlines()
    final_score_line = next((line for line in lines if "final score" in line.lower()), None)
    score = float(final_score_line.split(":")[1].strip()) if final_score_line else 0.0
    return EvaluationRecord(
        story_id=story_id,
        story_title=story_title,
        final_score=score,
        full_response={"raw_response": content}
    )