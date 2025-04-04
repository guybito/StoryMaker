"""
Plot Genie - Fiction Plot Generator

This module implements a class `PlotGenie` that generates random plot skeletons
based on the 1934 book "Plot Genie Index" by Wycliffe A. Hill.
It selects elements from predefined lists of story components such as locale,
characters, problems, obstacles, complications, predicaments, crises, and climaxes.

Key Features:
- Modular and extensible
- Supports reproducible randomness with seed
- Generates natural language plot summaries
- Can export plot descriptions to text files

Data source: JSON files containing the categorized plot elements.
"""

import json
import random
import os
import re

with open("Data/Thematic_Keywords.json", "r", encoding="utf-8") as f:
    THEMATIC_KEYWORDS = json.load(f)


def get_theme(*texts):
    """
    Identifies a thematic keyword category that matches any of the provided text inputs.
    Useful to maintain narrative consistency across categories like complications or crises.

    Args:
        *texts (str): Variable number of string inputs from which to extract theme.

    Returns:
        str or None: The name of the matched theme or None if no theme found.
    """
    combined_text = " ".join(texts).lower()
    for theme, keywords in THEMATIC_KEYWORDS.items():
        if any(kw in combined_text for kw in keywords):
            return theme
    return None


def filter_by_theme(category_list, theme):
    """
    Filters a list of story elements based on whether they match the given theme.
    If no items match, returns the full original list (fallback).

    Args:
        category_list (list): List of strings representing story elements.
        theme (str or None): Theme name to filter by.

    Returns:
        list: Filtered list of elements matching the theme, or full list if no match.
    """
    if not theme:
        return category_list
    filtered = [item for item in category_list if any(kw in item.lower() for kw in THEMATIC_KEYWORDS[theme])]
    return filtered if filtered else category_list


class PlotGenie:
    """
    PlotGenie class for generating random plot skeletons based on categorized story elements.

    Parameters:
        data_dir (str): Directory containing the JSON data files.
        seed (int, optional): Seed for random number generator for reproducibility.

    Methods:
        generate_plot(): Returns a dictionary with plot components, applying thematic filtering logic to categorize such as Complication, Predicament, Crisis, Climax, and Locale based on shared keywords extracted from the problem and obstacle.
        describe_plot(): Returns a human-readable description of the generated plot.
        save_plot_to_file(): Saves the plot description to a text file.
    """

    def __init__(self, data_dir="Data", seed=None):
        self.last_plot_description = None
        if seed is not None:
            random.seed(seed)
        self.data_dir = data_dir
        self.locale = self.load_json("Locale.json")
        self.hero = self.load_json("Usual_Male_Characters.json") + self.load_json("Unusual_Male_Characters.json")
        self.beloved = self.load_json("Usual_Female_Characters.json") + self.load_json("Unusual_Female_Characters.json")
        self.problems = self.load_multiple_jsons([
            "Problems_1.json", "Problems_2.json", "Problems_3.json",
            "Problems_4.json", "Problems_5.json", "Problems_6.json"
        ])
        self.obstacles = self.load_json("Obstacles_To_Love.json")
        self.complications = self.load_json("Complications.json")
        self.predicaments = self.load_json("Predicaments.json")
        self.crises = self.load_json("Crises.json")
        self.climaxes = self.load_json("Climaxes_Surprise_Twists.json")

    def load_json(self, filename):
        """Load a single JSON file from the data directory."""
        path = os.path.join(self.data_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_multiple_jsons(self, filenames):
        """Load and combine multiple JSON files into a single list."""
        combined = []
        for filename in filenames:
            combined.extend(self.load_json(filename))
        return combined

    def generate_plot(self, show_theme=False, save=False):
        """Randomly select one element from each story category to form a plot."""
        # Choose random values for required plot components
        hero = random.choice(self.hero)
        beloved = random.choice(self.beloved)
        problem = random.choice(self.problems)
        obstacle = random.choice(self.obstacles)
        # Derive the theme from both problem and obstacle text
        theme = get_theme(problem, obstacle)
        if show_theme and theme:
            print(f"🧠 Identified theme: {theme}")

        complication = random.choice(filter_by_theme(self.complications, theme))
        predicament = random.choice(filter_by_theme(self.predicaments, theme))
        crisis = random.choice(filter_by_theme(self.crises, theme))
        locale = random.choice(filter_by_theme(self.locale, theme))
        climax = random.choice(filter_by_theme(self.climaxes, theme))

        plot = {
            "Locale": locale,
            "Hero": hero,
            "Beloved": beloved,
            "Problem": problem,
            "Obstacle": obstacle,
            "Complication": complication,
            "Predicament": predicament,
            "Crisis": crisis,
            "Climax": climax,
        }

        self.last_plot_description = (
            f"In this story set {plot['Locale'].lower()}, our hero is a {plot['Hero'].lower()} who falls in love with a {plot['Beloved'].lower()}...\n"
            f"Their goal is blocked by a major problem: {plot['Problem'].lower()}.\n"
            f"However, love does not come easy because {plot['Obstacle'].lower()}.\n"
            f"Things become more tangled when {plot['Complication'].lower()},\n"
            f"and matters worsen as {plot['Predicament'].lower()}.\n"
            f"At the height of tension, a crisis hits: {plot['Crisis'].lower()}.\n"
            f"The story climaxes in a twist where {plot['Climax'].lower()}\n"
        )

        # Optionally save the generated plot to a new text file
        if save:
            self.save_plot_to_file(theme=theme)
        return plot

    def describe_plot(self):
        """Return the latest plot description in story format, with an introductory header."""
        header = "📖 Here is your generated plot:\n" + "=" * 35 + "\n"
        return header + getattr(self, 'last_plot_description', "No plot generated yet.")

    def save_plot_to_file(self, theme=None):
        """Automatically save the last generated plot description to a numbered text file."""
        directory = "Plot Genie Plots"
        os.makedirs(directory, exist_ok=True)

        existing = [file for file in os.listdir(directory) if file.startswith("Plot_") and file.endswith(".txt")]
        number_pattern = re.compile(r"Plot_(\d+)(?:_.*?)?\.txt")
        numbers = []

        for file in existing:
            match = number_pattern.match(file)
            if match:
                numbers.append(int(match.group(1)))

        next_number = max(numbers, default=0) + 1

        if theme:
            theme_safe = theme.replace(" ", "_").lower()
            filename = f"Plot_{next_number}_{theme_safe}.txt"
        else:
            filename = f"Plot_{next_number}.txt"

        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(self.last_plot_description)

        print(f"📚 Plot saved to: {filepath}")
