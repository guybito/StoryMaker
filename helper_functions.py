import os


def save_story_to_file(title: str, story: str):
    folder_name = "Stories"
    os.makedirs(folder_name, exist_ok=True)

    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    file_path = os.path.join(folder_name, f"{safe_title}.txt")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(story)

    print(f"Story saved to: {file_path}")
    return file_path


def extract_title(text):
    for line in text.splitlines():
        if line.strip().startswith('#'):
            return line.replace('#', '').replace('*', '').strip()
    return None


def read_story(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    title = extract_title(text)

    story_lines = text.splitlines()
    story_body = '\n'.join(line for line in story_lines if not line.strip().startswith('#')).strip()

    return title, story_body


def save_evaluation_report_to_file(story_id: int, story_title: str, content: str, directory="Reports"):
    os.makedirs(directory, exist_ok=True)

    filename = f"{story_id}_{story_title.replace(' ', '_')}_Report.txt"
    file_path = os.path.join(directory, filename)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"📘 Story Title: {story_title}\n")
        file.write(f"🆔 Story ID: {story_id}\n")
        file.write(f"{'-' * 60}\n")
        file.write("📄 Claude Evaluation Report\n")
        file.write(f"{'-' * 60}\n\n")
        file.write(content.strip())

    print(f"✅ Evaluation report saved to: {file_path}")
    return file_path
