import claude_service
import helper_functions


def build_full_review_based_prompt(story_file_path: str, evaluation_file_path: str) -> str:
    with open(story_file_path, 'r', encoding='utf-8') as story_file:
        story_text = story_file.read()

    with open(evaluation_file_path, 'r', encoding='utf-8') as eval_file:
        evaluation_text = eval_file.read()

    # prompt = (
    #     "You are a senior literary editor and narrative specialist. Your task is to analyze and revise a literary story using an expert evaluation and critique provided to you.\n\n"
    #     "You have received the following two essential inputs:\n"
    #     "1. The full original version of the story.\n"
    #     "2. A complete evaluation report including detailed question-by-question analysis and a section with suggested improvements based on literary criteria.\n\n"
    #     "Your job is to rewrite and refine the story based on the critique and recommendations. Use your editorial judgment to preserve the story's core voice and meaning while improving structure, clarity, emotional resonance, pacing, and narrative quality.\n\n"
    #     "Make sure to:\n"
    #     "- Integrate relevant suggestions from the evaluation.\n"
    #     "- Keep the revised story aligned with the original's spirit and themes.\n\n"
    #     "You may rewrite whole sections where appropriate, but aim to preserve and elevate the author's intent.\n\n"
    #     "----- ORIGINAL STORY -----\n"
    #     f"{story_text.strip()}\n\n"
    #     "----- FULL EVALUATION REPORT -----\n"
    #     f"{evaluation_text.strip()}\n\n"
    #     "Now, please rewrite and improve the story based on the evaluation above. The result should be a refined, high-quality version ready for literary publication."
    # )

    prompt = (
        "You are a senior literary editor and narrative specialist. Your task is to revise a literary story using a detailed evaluation report and critique that analyzes the story across multiple literary dimensions.\n\n"
        "The evaluation report you will receive follows a structured format consisting of:\n"
        "- A question-by-question breakdown grouped under categories such as Character, Conflict, Craft, and Logic.\n"
        "- Each question includes a score (0–4), a weight, and a brief explanation.\n"
        "- At the end of the report, there is a summary section titled 'Suggestions for Improvement', which synthesizes the most important actionable changes to enhance the story.\n\n"
        "Your objective is to rewrite and improve the story based specifically on the suggestions in the 'Suggestions for Improvement' section.\n"
        "However, if you notice recurring low scores or critique points in other sections (like character depth, escalation of conflict, logic issues, etc.), feel free to address them as well.\n\n"
        "You must:\n"
        "- Carefully read and understand the 'Suggestions for Improvement'.\n"
        "- Apply those suggestions throughout the revised story.\n"
        "- Ensure the rewritten story preserves the author's voice and original intent.\n"
        "- Improve clarity, pacing, character depth, emotional tone, logical consistency, and narrative momentum where needed.\n\n"
        "Do NOT summarize or comment on the story or evaluation. Do NOT explain your changes.\n\n"
        "Your output should be only the full revised story, formatted as follows:\n"
        "- Begin with a title in Markdown format, like: '# *Your Story Title*'\n"
        "- Then include the full narrative text below, properly structured as a readable literary story.\n"
        "- Do not include any commentary, summary, bullet points, or explanation — only the revised story.\n\n"
        "----- ORIGINAL STORY -----\n"
        f"{story_text.strip()}\n\n"
        "----- FULL EVALUATION REPORT -----\n"
        f"{evaluation_text.strip()}\n\n"
        "Now, please rewrite the story to address the issues raised in the report above—especially the 'Suggestions for Improvement' section—and produce a polished version suitable for publication."
    )

    return prompt


if __name__ == "__main__":
    prompt = build_full_review_based_prompt("../Claude_Stories/TestStory5555.txt","../backend/Reports/0_The_Apple_that_Whispered_Fire_Report.txt")
    response = claude_service.send_prompt_to_claude(prompt)
    story_title = helper_functions.extract_title(response) + "_improved"
    helper_functions.save_story_to_file(story_title, response)
    print(response)