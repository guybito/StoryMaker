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


class PlotGenieBasic:
    """
    PlotGenie class for generating random plot skeletons based on categorized story elements.

    Parameters:
        data_dir (str): Directory containing the JSON data files.
        seed (int, optional): Seed for random number generator for reproducibility.

    Methods:
        generate_plot(): Returns a dictionary with randomly selected plot components.
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
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_multiple_jsons(self, filenames):
        """Load and combine multiple JSON files into a single list."""
        combined = []
        for filename in filenames:
            combined.extend(self.load_json(filename))
        return combined

    def generate_plot(self, save=False):
        """Randomly select one element from each story category to form a plot."""
        plot = {
            "Locale": random.choice(self.locale),
            "Hero": random.choice(self.hero),
            "Beloved": random.choice(self.beloved),
            "Problem": random.choice(self.problems),
            "Obstacle": random.choice(self.obstacles),
            "Complication": random.choice(self.complications),
            "Predicament": random.choice(self.predicaments),
            "Crisis": random.choice(self.crises),
            "Climax": random.choice(self.climaxes),
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
        if save:
            self.save_plot_to_file()
        return plot

    def describe_plot(self):
        """Return the latest plot description in story format."""
        header = "📖 Here is your generated plot:\n" + "=" * 35 + "\n"
        return header + getattr(self, 'last_plot_description', "No plot generated yet.")

    def save_plot_to_file(self):
        """Automatically save the last generated plot description to a numbered text file."""
        directory = "Plot Genie Plots"
        os.makedirs(directory, exist_ok=True)

        existing = [f for f in os.listdir(directory) if f.startswith("Plot_") and f.endswith(".txt")]
        numbers = [int(f[5:-4]) for f in existing if f[5:-4].isdigit()]
        next_number = max(numbers, default=0) + 1

        filename = f"Plot_{next_number}.txt"
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.last_plot_description)

        print(f"📚 Plot saved to: {filepath}")
