# 📚 Plot Genie

A Python-based generator for story skeletons, inspired by the classic 1934 book *"Plot Genie Index"* by Wycliffe A. Hill. This tool creates randomized yet genre-aligned plot structures and generates rich story prompts suitable for AI storytelling systems.

---

## 🚀 Features

- Generates plot outlines from 9 categories: Locale, Hero, Beloved, Problem, Obstacle, Complication, Predicament, Crisis, Climax.
- Supports 5 genres: Romance, Adventure, Mystery, Comedy, Dramatic.
- Filters elements using semantic embeddings to better match the chosen genre.
- Automatically formats full prompts based on selected story length.
- Optional saving of both plot and prompt to uniquely numbered `.txt` files.
- Built-in CLI for easy use.

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com//plot-genie.git
cd plot-genie
```

1. Create and activate a virtual environment (optional):
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

1. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📝 Requirements

Ensure these Python packages are installed:
```
sentence-transformers==2.2.2
torch>=1.6.0
scikit-learn
numpy
nltk
tqdm
```

---

## 🧠 How It Works

- When a genre is selected, it is converted to a semantic embedding.
- All story elements (preprocessed with embeddings) are filtered using cosine similarity.
- A random item passing the similarity threshold (default 0.2) is selected per category.
- Genre-specific templates create fluent plot skeletons in natural language.
- The plot is used to generate an AI writing prompt with detailed literary instructions.

---

## 🛠️ Usage

### Run via CLI:

```bash
python cli_main.py
```

You’ll be prompted to:
- Choose a genre (random or manual)
- Choose desired word count
- Optionally save output to `.txt` files

### Programmatic Use:

```python
from PlotGenie import PlotGenie

genie = PlotGenie()
plot = genie.generate_plot(genre="Adventure", save=True)
prompt = genie.generate_adaptive_prompt(word_count=2000, generate_plot=False)
print(prompt)
```

---

## 🗃 Output Files

- `Plot Genie Plots/` – saved story skeletons
- `Plot Genie Prompts/` – full writing prompts for AI models

---


## 📌 Notes

- Precomputed embeddings stored in `with_embeddings/` for fast loading.
- Filter fallback: if no match is found, random choice ensures generation never fails.
- CLI script: `cli_main.py`

---