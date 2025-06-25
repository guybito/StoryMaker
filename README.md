# 📖 StoryMaker

**StoryMaker** is an automated story generation system that uses AI to create long-form narratives based on plot logic or skeleton prompts. It also supports automatic literary critique, iterative improvements, and generates clean HTML outputs for easy reading.

---

## 🚀 Features

- **Two plot generation algorithms**:
  - `Plotto`: Rule-based plot generation using recursive conflict resolution and character logic.
  - `PlotGenie`: Prompt-based skeleton generation expanded via AI.
- **Story creation** with adjustable length (word count).
- **Literary evaluation** using Claude 3.7.
- **Automated story improvement** based on critique feedback.
- **HTML export** for visually formatted story output and reports.

---

## 📂 Project Structure

```
StoryMaker/
├── main.py                     # Main execution file
├── claude_service.py           # Handles communication with Claude model
├── helper_functions.py         # Utility functions: save, extract titles, etc.
├── HTML/                       # HTML generation utilities
├── Plotto/                     # Plotto-based story generator
├── PlotGenie/                  # PlotGenie-based story generator
├── AutomatedLiteraryCritique/ # Evaluation and improvement engine
├── ScoreCalcAnalysis.py       # Analysis logic on story/report scores
└── Plotto/data/                # JSON files for character names, gender/pronoun maps, clauses
```

---

## ✅ Installation

1. Clone the repository:

```bash
git clone https://github.com/guybito/StoryMaker.git
cd StoryMaker
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** Make sure you have access to Claude 3.7 API and that your credentials are set properly in `claude_service.py`.

---

## 🧠 Usage

You can run the main script with different configurations:

```bash
python main.py
```

Or edit the bottom of `main.py` to select generation options:

```python
mainFlow("Plotto", stories_amount=1, words_in_story_amount=100, improve=False, create_html=True)
mainFlow("PlotGenie", stories_amount=1, words_in_story_amount=100, improve=False, create_html=True)
```

### Parameters

- `algorithm_type`: `"Plotto"` or `"PlotGenie"`
- `stories_amount`: Number of stories to generate
- `words_in_story_amount`: Approximate length per story
- `improve`: Whether to apply literary improvements
- `create_html`: Whether to generate `.html` versions of outputs

---

## 🧪 Output Files

For each story, the following files are generated:

- `.txt`: Raw story content
- `.txt`: Literary critique report
- `_improved.txt`: (Optional) Improved version of the story
- `.html`: (Optional) HTML version of the story and report

---

## 📊 Analysis

After generation, score analysis is performed automatically via `ScoreCalcAnalysis.py`.

---

## 🧑‍💻 Authors

Developed by [Dan Vaitzman](https://github.com/DanVaitzman1), [Guy Biton](https://github.com/guybito), [Tomer Katzav](https://github.com/kattomer), [Ido Dai](https://github.com/IdoDai)

AI story and critique powered by [Claude 3.7](https://www.anthropic.com/).

