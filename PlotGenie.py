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
        self.chosen_elements_index = []

    def get_genre(self, random_genre=True):
        if random_genre:
            return random.choice(self.genres)
        else:
            # TODO: if we want to let the user choose the genre - change it here
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
        for i in range(0, len(category_elements)):
            element_embedding = model.encode(category_elements[i], convert_to_tensor=True)
            similarity = util.cos_sim(element_embedding, genre_embedding).item()
            if similarity > 0.2:
                sim_res.append((i, similarity))
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

    def load_original_data(self):
        """Load the original data from the utils directory."""
        locale = self.load_json("Locale.json")

        hero = self.load_multiple_jsons(["Usual_Male_Characters.json", "Unusual_Male_Characters.json"])
        beloved = self.load_multiple_jsons(["Usual_Female_Characters.json", "Unusual_Female_Characters.json"])
        problems = self.load_multiple_jsons([
            "Problems_1.json", "Problems_2.json", "Problems_3.json",
            "Problems_4.json", "Problems_5.json", "Problems_6.json"
        ])
        obstacles = self.load_json("Obstacles_To_Love.json")
        complications = self.load_json("Complications.json")
        predicaments = self.load_json("Predicaments.json")
        crises = self.load_json("Crises.json")
        climaxes = self.load_json("Climaxes_Surprise_Twists.json")

        res = []
        res.append(locale[self.chosen_elements_index[0]])
        res.append(hero[self.chosen_elements_index[1]])
        res.append(beloved[self.chosen_elements_index[2]])
        res.append(problems[self.chosen_elements_index[3]])
        res.append(obstacles[self.chosen_elements_index[4]])
        res.append(complications[self.chosen_elements_index[5]])
        res.append(predicaments[self.chosen_elements_index[6]])
        res.append(crises[self.chosen_elements_index[7]])
        res.append(climaxes[self.chosen_elements_index[8]])
        return res


    def generate_plot(self, show_theme=False, save=False):
        """Randomly select one element from each story category to form a plot."""
        # Choose random values for required plot components
        genre = self.get_genre()
        for category in self.category_mapping.keys():
            element = self.filter_by_genre(category, genre)
            self.chosen_elements_index.append(element[0])

        res = self.load_original_data()

        plot = {
            "Genre": genre,
            "Locale": res[0],
            "Hero": res[1],
            "Beloved": res[2],
            "Problem": res[3],
            "Obstacle": res[4],
            "Complication": res[5],
            "Predicament": res[6],
            "Crisis": res[7],
            "Climax": res[8],
        }

        self.last_plot_description = (
            f"Genre: {plot['Genre']}\n"
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

    def generate_adaptive_prompt(self, word_count):
        """
        Generate an English prompt instructing an AI to write a full-length story based on a plot.

        Args:
            word_count (int): Desired word count for the final story.

        Returns:
            str: A rich prompt suitable for feeding into an AI writing model.
        """

        # TODO: Right now there is genre in the plot_text, if not helpful for the prompt, remove it.
        if not self.last_plot_description:
            return "No plot has been generated yet. Please run generate_plot() first."
        plot_text = self.last_plot_description

        # Adjust narrative guidelines based on word count
        if word_count <= 1500:
            instructions = (
                "- Keep the story concise and impactful.\n"
                "- Focus on a single main character and conflict.\n"
                "- Avoid too many subplots or detailed backstory.\n"
            )
        elif word_count <= 4000:
            instructions = (
                "- Focus on one or two characters with light emotional development.\n"
                "- Include a clear central conflict and resolution.\n"
                "- Use minimal dialogue and description.\n"
            )
        elif word_count <= 10000:
            instructions = (
                "- Include meaningful character development.\n"
                "- Introduce at least one subplot or side character.\n"
                "- Use dialogue and emotion to deepen the story.\n"
            )
        elif word_count <= 20000:
            instructions = (
                "- Develop rich character arcs and relationships.\n"
                "- Include multiple turning points or dramatic sequences.\n"
                "- Balance narration, action, and dialogue.\n"
            )
        else:
            instructions = (
                "- Craft a full, multi-layered narrative with depth and detail.\n"
                "- Include several subplots and diverse characters.\n"
                "- Explore themes, internal struggles, and a satisfying resolution.\n"
            )

            # Advanced writing criteria inspired by literary review standards
        advanced_criteria = (
            "Additionally, ensure the story meets high literary standards across four dimensions:\n"
            "CHARACTER:\n"
            "- Ensure the main character is clearly identifiable and undergoes a meaningful arc.\n"
    
            "- Provide clear goals, backstory, and internal vulnerability.\n"
            
            "- Make supporting characters diverse and distinct, each serving a clear role.\n"
            
            "- Show characters' psychological, social, and physical dimensions.\n"
                        
            "CONFLICT:\n"
            
            "- Present a strong central conflict that escalates over time.\n"
            
            "- Ensure the stakes are clear and relatable to universal human experiences.\n"
            
            "- Include both internal (emotional) and external (event-based) conflicts.\n"
            
            "- Keep the source of conflict consistent throughout the story.\n"

            "CRAFT:\n"
            
            "- Use clear, modern English. Maintain excellent grammar and sentence structure.\n"
            
            "- Describe characters, setting, and actions vividly and concisely.\n"
            
            "- Avoid unnecessary details, and make descriptions visual and demonstrable.\n"
            
            "LOGIC:\n"
            
            "- Avoid plot holes or contradictions.\n"
            
            "- Make sure all questions are resolved and events flow logically.\n"

        )

        # Add title request and language specification
        title_request = (
            "Give the story an appropriate, compelling title.")
        language_request = (
            "Write the entire story in clear, modern English. Avoid archaic expressions.")

        return (
            f"Write a story of approximately {word_count} words.\n"
            f"{title_request}\n"
            f"{language_request}\n"
            f"The story is based on the following plot skeleton:\n"
            f"{plot_text}"
            f"Use the plot above to craft a complete narrative with the following guidelines:\n"
            f"{instructions}"
            f"- Describe the setting and emotional tone.\n"
            f"- Emphasize the central conflict.\n"
            f"- Use natural dialogue where appropriate.\n"
            f"- You may expand on events while remaining faithful to the plot.\n"
            f"Aim for a smooth and engaging narrative voice. A dramatic or open ending is welcome.\n"
            f"{advanced_criteria}"
        )

    # TODO: Add when we got an API Key
    # def send_prompt_to_claude(self, word_count, api_key, model="claude-3-opus-20240229", save_to_file=False):
    #     """
    #     Sends the generated prompt to Claude via Anthropic API and returns the story.
    #
    #     Args:
    #         word_count (int): Target word count for the story.
    #         api_key (str): Your Anthropic Claude API key.
    #         model (str): Claude model ID (default: claude-3-opus-20240229).
    #         save_to_file (bool): Whether to save the generated story to a file.
    #
    #     Returns:
    #         str: Generated story text from Claude.
    #     """
    #     prompt = self.generate_adaptive_prompt(word_count)
    #     if prompt.startswith("No plot"):
    #         return prompt
    #
    #     response = requests.post(
    #         url="https://api.anthropic.com/v1/messages",
    #         headers={
    #             "x-api-key": api_key,
    #             "anthropic-version": "2023-06-01",
    #             "content-type": "application/json"
    #         },
    #         json={
    #             "model": model,
    #             "max_tokens": 4096,
    #             "messages": [{"role": "user", "content": prompt}]
    #         }
    #     )
    #
    #     if response.status_code == 200:
    #         data = response.json()
    #         self.last_story_text = data['content'][0]['text'] if data.get('content') else None
    #         if save_to_file:
    #             self.save_story_to_file()
    #         return self.last_story_text if self.last_story_text else "No story generated."
    #     else:
    #         return f"❌ Request failed with status {response.status_code}: {response.text}"

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
