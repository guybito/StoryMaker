from fastapi import FastAPI, HTTPException
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
    sample_story = (
        "The sharp winter wind carried whispers of conspiracy through the streets of Verona as Evan Blackwood walked briskly toward the city's grand courthouse. "
        "His tailored suit and commanding presence spoke of old money and influence—an aristocrat whose family had shaped the region's politics for generations. Yet today, his usual confidence was tempered by a growing sense of unease.\n\n"
        "\"The Duke requests your presence immediately, sir,\" his secretary had informed him earlier. Such an unexpected summons could only mean one thing—Leo Marconi's machinations were finally bearing fruit.\n\n"
        "Leo, once Evan's childhood friend and now his bitter rival, had spent years systematically undermining Evan's position in society. What few knew was that their enmity stemmed not from politics but from the heart. Both men had fallen for the captivating Danielle Laurent, whose beauty was matched only by her intellect. While Evan had courted her openly and honorably, Leo had won her affections through charm and calculated deception.\n\n"
        "\"I've chosen Leo,\" Danielle had told Evan six months ago, her eyes filled with apology. \"He understands me in ways you never could.\"\n\n"
        "What Danielle didn't know was that Leo was neck-deep in criminal enterprises, laundering money through his legitimate businesses while secretly trafficking contraband. Evan had discovered this ugly truth but kept silent, knowing revealing it would devastate Danielle. Now, that silence had become his undoing.\n\n"
        "As Evan approached the courthouse steps, guards surrounded him. \"Evan Blackwood, you are under arrest for conspiracy against the state,\" announced the captain, loud enough for the gathering crowd to hear.\n\n"
        "Leo watched from across the square, a thin smile playing on his lips as Evan's gaze met his. In that moment, Evan understood—the evidence against him had been fabricated by Leo himself.\n\n"
        "The trial was a farce. Falsified documents linked Evan to radical separatists, while paid witnesses testified to meetings that never occurred. The sentence was swift and severe: death by execution at dawn.\n\n"
        "That night, with the help of his loyal servant, Evan escaped imprisonment. Knowing he couldn't clear his name while remaining in Verona, he fled across the border to the notorious city of Blackwater, a haven for outcasts and criminals.\n\n"
        "There, Evan shed his aristocratic identity, adopting the persona of \"Rook,\" a rough-edged criminal with a talent for strategy. He grew a beard, dirtied his once-immaculate hands, and learned the language of the streets. The transformation was complete when he began moving among thieves and smugglers, gathering intelligence while building a network of his own.\n\n"
        "\"You've got a knack for this work,\" commented Silas, an aging fence who had taken a liking to Rook. \"Almost as if you were born to a different life.\"\n\n"
        "From the shadows, Evan monitored Leo's expanding criminal empire and his relationship with Danielle. With each passing month, his plan for vengeance grew more refined. Not content with merely exposing Leo, Evan meticulously documented his rival's crimes while placing his own agents within Leo's organization.\n\n"
        "When Danielle finally discovered Leo's true nature—finding incriminating documents that Evan had ensured would reach her—she confronted her lover. Leo, sensing his carefully constructed world crumbling, arranged for her silence through permanent means.\n\n"
        "The night Leo's men came for Danielle, they found not a vulnerable woman but a trap sprung by Rook and his allies. As Leo was publicly exposed, the web of evidence Evan had gathered was anonymously delivered to the authorities.\n\n"
        "In the chaos that followed, Evan revealed himself to Danielle. \"I could have simply killed him,\" he explained, \"but that would have made me no better than he is.\"\n\n"
        "\"Why risk everything for me?\" she asked, truly seeing him for the first time.\n\n"
        "\"Because some principles matter more than vengeance,\" Evan replied as he turned toward the approaching authorities.\n"
    )
    result = generate_claude_evaluation_report(
        story_id=123,
        story_title="Test Story",
        story_text=sample_story
    )
    print("Evaluation result:", result)
    input("Press Enter to exit...")

