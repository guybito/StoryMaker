import anthropic
from pathlib import Path

import claude_service
from claude_service import *

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "evaluation_prompt.txt", "r", encoding="utf-8") as f:
    CRITERIA_PROMPT = f.read()


def generate_claude_evaluation_report(story_id: int, story_title: str, story_text: str) -> dict:
    prompt = CRITERIA_PROMPT.format(story=story_text, title=story_title, id=story_id)
    content = claude_service.send_prompt_to_claude(prompt)
    # response = anthropic_client.messages.create(
    #     model="claude-3-7-sonnet-20250219",
    #     max_tokens=20000,
    #     temperature=0.3,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # if not response or not response.content or not response.content[0].text.strip():
    #     raise ValueError("Empty or invalid response from Claude.")
    #
    # content = response.content[0].text
    return _parse_response(story_id, story_title, content)


def _parse_response(story_id: int, story_title: str, content: str):
    lines = content.splitlines()
    final_score_line = next((line for line in lines if "Overall Weighted Score" in line.lower()), None)
    score = float(final_score_line.split(":")[1].strip()) if final_score_line else 0.0

    print("📝 Claude Raw Response:")
    print(content)
    print("\n✅ Parsed Result:")
    print(f"Story ID: {story_id}")
    print(f"Story Title: {story_title}")
    print(f"Final Score: {score}")

    return {
        "story_id": story_id,
        "story_title": story_title,
        "final_score": score,
        "raw_response": content
    }
