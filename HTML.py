import os

def convert_story_to_html(input_file_path: str, output_filename: str = "story.html"):

    output_dir = "STORY_TO_SHOW"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_lines = ["<!DOCTYPE html>", "<html lang='en'>", "<head>", "<meta charset='UTF-8'>",
                  "<meta name='viewport' content='width=device-width, initial-scale=1.0'>", "<title>Story</title>", """
    <style>
        body {
            font-family: 'Georgia', serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fefefe;
            color: #222;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 40px;
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
        }
        p {
            text-align: justify;
            margin-bottom: 20px;
        }
    </style>
    """, "</head>", "<body>"]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        elif stripped.startswith("# *") and stripped.endswith("*"):
            title = stripped.replace("# *", "").replace("*", "").strip()
            html_lines.append(f"<h1>{title}</h1>")
        else:
            html_lines.append(f"<p>{stripped}</p>")

    html_lines.append("</body>")
    html_lines.append("</html>")

    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))

    print(f"✔ סיפור הומר ונשמר בהצלחה תחת: {output_path}")


if __name__ == "__main__":
    convert_story_to_html("Stories/Stars in the Machine_improved.txt","StarsInTheMachine.html")