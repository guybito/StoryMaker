import openai
import anthropic
import google.generativeai as genai
from schemas import EvaluationRecord

openai.api_key = "YOUR_OPENAI_API_KEY"
anthropic_client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

CRITERIA_PROMPT = """
You are a professional literary critic. Please analyze the following short story and evaluate it using 30 detailed questions.

For each question, provide:
- The question text
- The score (0–4)
- The question weight (within its category)
- The category name
- The category weight (as part of the full evaluation)
- The weighted score, calculated as:
  Weighted Score = Score × Question Weight × Category Weight
- A brief explanation (1–2 sentences) justifying the score based on the story(example : informative explanation with examples from the story )

Use this exact structure for each row. Then, calculate:
1. The sum of all weighted scores (should range from 0 to 4.0).
2. A short report (3–5 sentences).
3. Three suggestions to improve the story based on weak points.

---

### CATEGORIES AND QUESTIONS:

**Character (Category Weight = 0.30)**
1. (0.15) Is the main character clearly identifiable? If the story has two central characters, are both clearly identifiable? If it's an ensemble story, consider the following questions for each main character.
2. (0.10) Does the character have a clear backstory?
3. (0.10) Does the character have a clear goal or "desire"? Is the character actively pursuing this goal?
4. (0.10) Does the character have a clear inner weakness, fear, vulnerability, or internal need distinct from their external goal? Are there moments when the character is vulnerable or giving, allowing us to identify with them?
5. (0.10) Does the character undergo a transformation (learning a lesson or overcoming a weakness) that completes their narrative arc?
6. (0.10) Does each supporting character significantly contribute to challenging, advancing, or helping the main character on their journey or growth?
7. (0.10) Do the supporting characters fulfill typical or archetypal roles (e.g., attractor, ally, mentor, messenger, antagonist/villain, etc.)? If there is a villain, do they effectively contrast with the main character in terms of values, strengths, motivations, or ideology?
8. (0.10) Are the supporting characters diverse, distinct from each other, and distinct from the main character?
9. (0.10) Is the number of characters appropriate for the narrative (not too many)?
10. (0.05) Are characters developed across the following three layers? (Physical/external, Mental/psychological, Social/sociological)

**Conflict (Category Weight = 0.30)**
11. (0.35) Is the central conflict strong enough to drive the story and keep the main character sufficiently challenged throughout?
12. (0.15) Does the conflict touch upon universal human conditions? Can a broad audience relate, having faced similar conflicts themselves?
13. (0.10) Are the stakes clear from the beginning? Are they credible within the context of the conflict?
14. (0.10) Is the conflict directly related to what we know about the character?
15. (0.10) Does the conflict escalate and intensify as the story approaches its climax?
16. (0.10) Is the source of the conflict consistent throughout?
17. (0.05) Do the subplots also include conflict?
18. (0.05) Is there both external conflict (events) and internal conflict (emotions)?

**Craft (Category Weight = 0.25)**
19. (0.20) Is the story written in clear, modern English?
20. (0.15) Are spelling and grammar correct? Are sentences grammatically and syntactically correct? Are sentence structures and order clear? Are there any typos or spelling errors? (Minor issues such as missing commas are not critical.)
21. (0.15) Is the writing clear, concise, and descriptive? (Not confusing, overly long, or lacking necessary details.)
22. (0.15) Is there a vivid and accurate description of the main characters, memorable scenes, and a clear geographical setting? Is there effective use of descriptive language to create atmosphere, visual imagery, and engaging depictions of movements and events? Is the writing impressive, sophisticated, and skillful?
23. (0.15) Is there no unnecessary or inappropriate detail?
24. (0.20) Is everything described visually demonstrable, or are there too many descriptions that can't be captured visually (e.g., thoughts, emotional states, etc.)?

**Logic (Category Weight = 0.15)**
25. (0.20) Are there no plot holes?
26. (0.20) Are there no unclear points?
27. (0.15) Have all questions raised been answered (no loose ends)?
28. (0.15) Is the story consistent and free of continuity errors?
29. (0.15) Are there no contradictions with previously stated information?
30. (0.15) Is the logic sound and free from illogical or contrived elements?

---

STORY TO EVALUATE:
\"\"\"{story}\"\"\"
"""


async def generate_openai_evaluation_report(story_id: int, story_title: str, story_text: str) -> EvaluationRecord:
    prompt = CRITERIA_PROMPT.format(story=story_text)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message["content"]
    return _parse_response(story_id, story_title, content)


async def generate_claude_evaluation_report(story_id: int, story_title: str, story_text: str) -> EvaluationRecord:
    prompt = CRITERIA_PROMPT.format(story=story_text)
    response = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.content[0].text if response.content else ""
    return _parse_response(story_id, story_title, content)


async def generate_gemini_evaluation_report(story_id: int, story_title: str, story_text: str) -> EvaluationRecord:
    prompt = CRITERIA_PROMPT.format(story=story_text)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt, generation_config={"temperature": 0.3})
    content = response.text
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