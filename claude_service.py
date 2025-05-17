import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def send_prompt_to_claude(prompt=None, prompt_file=None, model="claude-3-7-sonnet-20250219"):
    """
       Sends a prompt to Claude-3 and returns the response text.
       You can provide the prompt as a string or via a text file.
       """
    if prompt_file:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()

    if not prompt:
        raise ValueError("You must provide a prompt string or a prompt_file.")

    try:
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=20000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_message = f"An error occurred while sending prompt to Claude: {str(e)}"
        print(error_message)
        return error_message


async def send_prompt_to_claude_async(prompt=None, prompt_file=None, model="claude-3-7-sonnet-20250219"):
    """
        Asynchronously sends a prompt to Claude-3 and returns the response text.
        Accepts input as a string or from a text file.
        """
    if prompt_file:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()

    if not prompt:
        raise ValueError("You must provide a prompt string or a prompt_file.")

    try:
        response = await anthropic_client.messages.create(
            model=model,
            max_tokens=20000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error sending request: {str(e)}"
