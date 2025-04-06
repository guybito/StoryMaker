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
from sentence_transformers import SentenceTransformer, util



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

    def __init__(self, data_dir="Utils", seed=None):
        self.last_plot_description = None
        self.genres = ['Romance', 'Adventure', 'Mystery', 'Comedy', 'Dramatic']
        if seed is not None:
            random.seed(seed)
        self.data_dir = data_dir
        self.locale = self.load_json("cleaned_Locale.json")
        self.hero = self.load_multiple_jsons(["cleaned_Usual_Male_Characters.json", "cleaned_Unusual_Male_Characters.json"])
        self.beloved = self.load_multiple_jsons(["cleaned_Usual_Female_Characters.json", "cleaned_Unusual_Female_Characters.json"])
        self.problems = self.load_multiple_jsons([
            "cleaned_Problems_1.json", "cleaned_Problems_2.json", "cleaned_Problems_3.json",
            "cleaned_Problems_4.json", "cleaned_Problems_5.json", "cleaned_Problems_6.json"
        ])
        self.obstacles = self.load_json("cleaned_Obstacles_To_Love.json")
        self.complications = self.load_json("cleaned_Complications.json")
        self.predicaments = self.load_json("cleaned_Predicaments.json")
        self.crises = self.load_json("cleaned_Crises.json")
        self.climaxes = self.load_json("cleaned_Climaxes_Surprise_Twists.json")
        self.category_mapping = {
            "locale": self.locale,
            "hero": self.hero,
            "beloved": self.beloved,
            "problems": self.problems,
            "obstacles": self.obstacles,
            "complications": self.complications,
            "predicaments": self.predicaments,
            "crises": self.crises,
            "climaxes": self.climaxes,
        }
        self.chosen_elements = []

    def get_genre(self, random_genre=True):
        if random_genre:
            return random.choice(self.genres)
        else:
            return None

    def get_category_elements(self, category):
        return self.category_mapping[category]

    def filter_by_genre(self, category, genre):
        """
        Filters a list of story elements based on whether they match the given theme.
        If no items match, returns the full original list (fallback).

        Args:
            category (string): String that represents the story elements.
            genre (string): genre name to filter by.

        Returns:
            list: Filtered list of elements matching the genre, or full list if no match.
        """
        if not genre:
            return self.get_category_elements(category)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        category_elements = self.category_mapping.get(category)
        genre_embedding = model.encode(genre, convert_to_tensor=True)
        sim_res = []
        for element in category_elements:
            element_embedding = model.encode(element, convert_to_tensor=True)
            similarity = util.cos_sim(element_embedding, genre_embedding).item()
            if similarity > 0.2:
                sim_res.append((element, similarity))
        return random.choice(sim_res)

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
        genre = self.get_genre()
        for category in self.category_mapping.keys():
            element = self.filter_by_genre(category, genre)
            self.chosen_elements.append(element[0])

        plot = {
            "Genre": genre,
            "Locale": self.chosen_elements[0],
            "Hero": self.chosen_elements[1],
            "Beloved": self.chosen_elements[2],
            "Problem": self.chosen_elements[3],
            "Obstacle": self.chosen_elements[4],
            "Complication": self.chosen_elements[5],
            "Predicament": self.chosen_elements[6],
            "Crisis": self.chosen_elements[7],
            "Climax": self.chosen_elements[8],
        }
        print(plot)
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
            self.save_plot_to_file(genre=genre)
        return plot

    def describe_plot(self):
        """Return the latest plot description in story format, with an introductory header."""
        header = "📖 Here is your generated plot:\n" + "=" * 35 + "\n"
        return header + getattr(self, 'last_plot_description', "No plot generated yet.")

    def save_plot_to_file(self, genre=None):
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

        if genre:
            theme_safe = genre.replace(" ", "_").lower()
            filename = f"Plot_{next_number}_{theme_safe}.txt"
        else:
            filename = f"Plot_{next_number}.txt"

        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(self.last_plot_description)

        print(f"📚 Plot saved to: {filepath}")
