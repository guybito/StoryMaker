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


def save_prompt_to_file(prompt):
    """
    Saves a generated AI prompt to a uniquely numbered text file.

    Args:
        prompt (str): The prompt string to be saved.
    """
    directory = "Plot Genie Prompts"
    os.makedirs(directory, exist_ok=True)

    existing = [file for file in os.listdir(directory) if file.startswith("Prompt_") and file.endswith(".txt")]
    number_pattern = re.compile(r"Prompt_(\d+)(?:_.*?)?\.txt")
    numbers = []

    for file in existing:
        match = number_pattern.match(file)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers, default=0) + 1
    filename = f"Prompt_{next_number}.txt"

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(prompt)

    print(f"📚 Prompt saved to: {filepath}")


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

    def __init__(self, data_dir="../StoryMaker/PlotGenie/Utils", seed=None):
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

    def generate_plot(self):
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

        # self.last_plot_description = (
        #     f"Locale: {plot['Locale'].lower()}\n"
        #     f"Hero: {plot['Hero'].lower()}\n"
        #     f"Beloved: {plot['Beloved'].lower()}\n"
        #     f"Problem: {plot['Problem'].lower()}\n"
        #     f"Obstacle: {plot['Obstacle'].lower()}\n"
        #     f"Complication: {plot['Complication'].lower()}\n"
        #     f"Predicament: {plot['Predicament'].lower()}\n"
        #     f"Crisis: {plot['Crisis'].lower()}\n"
        #     f"Climax: {plot['Climax'].lower()}\n"
        # )

        plot_string = (
            f"In this story set in a {plot['Locale'].lower()}, our main character is a {plot['Hero'].lower()}, accompanied by a key supporting figure, a {plot['Beloved'].lower()}.\n"
            f"Their shared objective faces a significant obstacle: {plot['Problem'].lower()}.\n"
            f"Progress becomes difficult due to {plot['Obstacle'].lower()}.\n"
            f"The situation grows more complex when {plot['Complication'].lower()},\n"
            f"and deteriorates further as {plot['Predicament'].lower()}.\n"
            f"Tension peaks when an unexpected crisis arises: {plot['Crisis'].lower()}.\n"
            f"The story reaches a turning point in a pivotal moment where {plot['Climax'].lower()}.\n"
        )
        
        return plot_string

    def describe_plot(self):
        """Return the latest plot description in story format."""
        header = "📖 Here is your generated plot:\n" + "=" * 35 + "\n"
        return header + getattr(self, 'last_plot_description', "No plot generated yet.")

    def generate_prompt(self, word_count, save=False):
        plot = self.generate_plot()

        prompt = f""" 
            Role: you are story writing expert
            The Plot:
            {plot}
            
            You are tasked with crafting an immersive and well-rounded story based on the provided plot 
            framework. This story should be in modern English, engaging, vivid, and address key aspects of storytelling effectively. Follow these instructions closely to ensure a superior narrative.
                                Story Requirements
                                1. Character Development
                                Clearly identify the protagonist and provide a compelling backstory that motivates their actions.
                                Define the protagonist's goal or "want," ensuring they take an active role in achieving it.
                                Include weaknesses, fears, or vulnerabilities that humanize the protagonist and make them relatable.
                                Show a clear arc of change for the protagonist, where they grow, learn a lesson, or address their weaknesses by the end.
                                Ensure supporting characters are distinct, colorful, and contribute meaningfully to the protagonist’s journey. Avoid stereotypes or unnecessary characters.
                                Develop characters physically, mentally, and socially to create a multidimensional cast.
                                2. Conflict
                                Define a main conflict that is challenging and relatable, ensuring it sustains tension throughout the story.
                                Relate the conflict to the human condition so it resonates with a broad audience.
                                Incorporate external events and internal emotional struggles for both the protagonist and supporting characters.
                                Introduce subplots with their own conflicts, which intertwine meaningfully with the main plot.
                                Escalate the conflict effectively toward the climax, and ensure it is fully resolved by the end.
                                3. Logic
                                Avoid plot holes or inconsistencies. Ensure every detail aligns with established facts in the story.
                                Clarify any potential ambiguities or unanswered questions to avoid reader confusion.
                                Ensure all major elements are consistent with the internal logic of the story.
                                4. Craft
                                Use modern, vivid English with sophisticated word choice to create vivid imagery.
                                Include rich descriptions of settings, characters, and actions to immerse readers in the story.
                                Ensure the writing is clear, concise, and grammatically correct.
                                5. Formatting Requirements
                                Write the story in clear, distinct paragraphs for better readability.
                                Provide a title that reflects the essence of the story.
                                Ensure the story spans around {word_count} words and delivers an engaging, complete narrative and being written in modern English
                                6. Title
                                write the title of the story at the beginning of the story, in the next format: *the real title of the story*
            """

        if save:
            save_prompt_to_file(prompt)

        return prompt
