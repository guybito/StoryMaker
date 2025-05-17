from fastapi import FastAPI, HTTPException

import helper_functions, os
from backend.literary_evaluation_engine import (generate_claude_evaluation_report)
from backend.schemas import EvaluationRecord
import asyncio

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


if __name__ == "__main__":
    title, story = helper_functions.read_story("../Plotto/Stories/The Blue Hat.txt")
    # print("Title:", title)
    # print("Story:\n", story)

    result = generate_claude_evaluation_report(
        story_id=9,
        story_title=title,
        story_text=story
    )
    helper_functions.save_evaluation_report_to_file(result["story_id"], result["story_title"], result["raw_response"])
    print("Evaluation result:", result)
    # input("Press Enter to exit...")

