"""
Plot Genie - Fiction Plot Generator

PlotGenie class that generates story plot outlines based on structured categories
derived from Wycliffe A. Hill’s 1934 "Plot Genie" system.
It selects elements from predefined lists of story components such as locale,
characters, problems, obstacles, complications, predicaments, crises, and climaxes.
Enhanced with semantic filtering via pre-trained sentence embeddings for genre alignment.

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
# from sentence_transformers import SentenceTransformer, util
from sentence_transformers import util


def save_prompt_to_file(prompt, genre=None):
    """
    Saves a generated AI prompt to a uniquely numbered text file.

    Args:
        prompt (str): The prompt string to be saved.
        genre (str, optional): Genre tag to include in the filename.
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

    if genre:
        theme_safe = genre.replace(" ", "_").lower()
        filename = f"Prompt_{next_number}_{theme_safe}.txt"
    else:
        filename = f"Prompt_{next_number}.txt"

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(prompt)

    print(f"📚 Prompt saved to: {filepath}")


class PlotGenie:
    """
    Initializes the PlotGenie object by loading categorized story elements and their
    semantic embeddings.

    Args:
        data_dir (str): Path to original story data (uncleaned or reference data).
        seed (int, optional): Random seed for reproducible plot generation.
    """

    def __init__(self, data_dir="Utils", seed=None):
        self.genre = None
        self.last_plot_description = None
        self.genres = ['Romance', 'Adventure', 'Mystery', 'Comedy', 'Dramatic']
        if seed is not None:
            random.seed(seed)
        self.cleaned_data_dir = 'Utils_Cleaned'
        self.data_dir = data_dir
        self.embedding_dir = "with_embeddings"

        self.locale = self.load_json("cleaned_Locale.json", self.cleaned_data_dir)
        self.hero = self.load_multiple_jsons(
            ["cleaned_Usual_Male_Characters.json", "cleaned_Unusual_Male_Characters.json"], self.cleaned_data_dir)
        self.beloved = self.load_multiple_jsons(
            ["cleaned_Usual_Female_Characters.json", "cleaned_Unusual_Female_Characters.json"], self.cleaned_data_dir)
        self.problems = self.load_multiple_jsons([
            "cleaned_Problems_1.json", "cleaned_Problems_2.json", "cleaned_Problems_3.json",
            "cleaned_Problems_4.json", "cleaned_Problems_5.json", "cleaned_Problems_6.json"
        ], self.cleaned_data_dir)
        self.obstacles = self.load_json("cleaned_Obstacles_To_Love.json", self.cleaned_data_dir)
        self.complications = self.load_json("cleaned_Complications.json", self.cleaned_data_dir)
        self.predicaments = self.load_json("cleaned_Predicaments.json", self.cleaned_data_dir)
        self.crises = self.load_json("cleaned_Crises.json", self.cleaned_data_dir)
        self.climaxes = self.load_json("cleaned_Climaxes_Surprise_Twists.json", self.cleaned_data_dir)
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
        self.embeddings_cache = {}
        self.genre_embeddings = self.load_genre_embeddings()
        # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.load_all_embeddings()

    def load_genre_embeddings(self):
        """
        Loads precomputed sentence embeddings for genres from disk.

        Returns:
            dict: Mapping of genre names to their embedding vectors.
        """
        path = os.path.join(self.embedding_dir, "genres_with_embeddings.json")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {item["text"]: item["embedding"] for item in data}

    def load_all_embeddings(self):
        """
        Loads all precomputed embeddings for each story category
        (e.g., locale, hero, problem...) into a dictionary cache.
        """
        for category, original_list in self.category_mapping.items():
            filename = f"cleaned_{category.capitalize()}_with_embeddings.json"
            path = os.path.join(self.embedding_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.embeddings_cache[category] = loaded

    def get_category_elements(self, category):
        """
        Retrieves the raw list of items for a given category.

        Args:
            category (str): The category to retrieve (e.g., 'hero').

        Returns:
            list: All elements from the selected category.
        """
        return self.category_mapping[category]

    def filter_by_genre(self, category, genre):
        """
        Filters elements in a category by cosine similarity to the selected genre.
        If no elements pass the threshold (currently hardcoded to 0.2), it falls
        back to full random selection.

        Args:
            category (str): Category name (e.g., 'complication').
            genre (str): The genre to match against (e.g., 'Mystery').

        Returns:
            tuple: (index, similarity score) of the selected item.
        """
        if not genre or category not in self.embeddings_cache:
            return random.choice(list(enumerate(self.category_mapping[category])))

        genre_embedding = self.genre_embeddings.get(genre)
        if genre_embedding is None:
            return random.choice(list(enumerate(self.category_mapping[category])))

        candidates = self.embeddings_cache[category]

        sim_res = []
        for i, item in enumerate(candidates):
            element_embedding = item["embedding"]
            similarity = util.cos_sim(genre_embedding, element_embedding).item()
            ### need to check the threshold ###
            if similarity > 0.2:
                sim_res.append((i, similarity))

        if sim_res:
            return random.choice(sim_res)
        else:
            return random.choice(list(enumerate(self.category_mapping[category])))

    def load_json(self, filename, directory):
        """
        Loads a single JSON file from the specified directory.

        Returns:
            list or dict: JSON-parsed contents.
        """
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_multiple_jsons(self, filenames, directory):
        """
        Loads and combines multiple JSON files from a directory.

        Returns:
            list: Concatenated list of items from all specified files.
        """
        combined = []
        for filename in filenames:
            combined.extend(self.load_json(filename, directory))
        return combined

    def load_original_data(self):
        """
        Reloads the original (pre-cleaned) data using the chosen indices
        from the filtered embedding-based selection. This ensures compatibility
        with legacy formatting and consistent indexing.

        Returns:
            list: Ordered list of selected plot components.
        """
        locale = self.load_json("Locale.json", self.data_dir)
        hero = self.load_multiple_jsons(["Usual_Male_Characters.json", "Unusual_Male_Characters.json"], self.data_dir)
        beloved = self.load_multiple_jsons(["Usual_Female_Characters.json", "Unusual_Female_Characters.json"],
                                           self.data_dir)
        problems = self.load_multiple_jsons([
            "Problems_1.json", "Problems_2.json", "Problems_3.json",
            "Problems_4.json", "Problems_5.json", "Problems_6.json"
        ], self.data_dir)
        obstacles = self.load_json("Obstacles_To_Love.json", self.data_dir)
        complications = self.load_json("Complications.json", self.data_dir)
        predicaments = self.load_json("Predicaments.json", self.data_dir)
        crises = self.load_json("Crises.json", self.data_dir)
        climaxes = self.load_json("Climaxes_Surprise_Twists.json", self.data_dir)

        res = [locale[self.chosen_elements_index[0]], hero[self.chosen_elements_index[1]],
               beloved[self.chosen_elements_index[2]], problems[self.chosen_elements_index[3]],
               obstacles[self.chosen_elements_index[4]], complications[self.chosen_elements_index[5]],
               predicaments[self.chosen_elements_index[6]], crises[self.chosen_elements_index[7]],
               climaxes[self.chosen_elements_index[8]]]

        return res

    def generate_plot(self, save=False, genre=None):
        """
        Generates a plot aligned semantically with a genre.

        Steps:
        - Selects a genre (random or user-defined).
        - Filters each category by similarity to the genre embedding.
        - Retrieves the original elements by their indices.
        - Constructs a full plot dictionary and a readable plot description.

        Args:
            save (bool): If True, saves the plot to disk.
            genre (str): Optional genre to use instead of random selection.

        Returns:
            dict: Dictionary containing structured plot components.
        """
        if genre is not None:
            self.genre = genre
        else:
            self.genre = random.choice(self.genres)
        # Choose random values for required plot components
        for category in self.category_mapping.keys():
            element = self.filter_by_genre(category, self.genre)
            self.chosen_elements_index.append(element[0])

        res = self.load_original_data()

        plot = {
            "Genre": self.genre,
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

        genre_templates = {
            "Romance": (
                "In this story set {locale}, our hero is a {hero} who falls in love with a {beloved}.\n"
                "Their goal is blocked by a major problem: {problem}.\n"
                "However, love does not come easy because {obstacle}.\n"
                "Things become more tangled when {complication},\n"
                "and matters worsen as {predicament}.\n"
                "At the height of tension, a crisis hits: {crisis}.\n"
                "The story climaxes in a twist where {climax}.\n"
            ),
            "Adventure": (
                "Set in {locale}, this tale follows a {hero} who embarks on a daring quest with a companion, {beloved}.\n"
                "Their mission is complicated by {problem}\n"
                "and made worse by {obstacle}.\n"
                "Unexpectedly, {complication} arises,\n"
                "leading them into {predicament}.\n"
                "As tension builds, a major crisis unfolds: {crisis}.\n"
                "The story culminates in a climactic moment where {climax}.\n"
            ),
            "Mystery": (
                "At {locale}, a {hero} investigates a puzzling mystery with the help of {beloved}.\n"
                "The case begins with {problem},\n"
                "and is complicated by {obstacle}.\n"
                "Clues lead them into {complication},\n"
                "and they face a difficult situation with {predicament}.\n"
                "The mystery deepens with a shocking crisis: {crisis}.\n"
                "The truth is finally revealed when {climax}.\n"
            ),
            "Comedy": (
                "In the humorous setting of {locale}, a quirky {hero} is constantly thrown off balance by {beloved}.\n"
                "It all starts with {problem},\n"
                "and becomes even more ridiculous with {obstacle}.\n"
                "Things spiral when {complication} happens,\n"
                "leading to {predicament}.\n"
                "Just when it couldn't get worse, {crisis} unfolds.\n"
                "The story ends with a hilarious twist where {climax}.\n"
            ),
            "Dramatic": (
                "Set in {locale}, a {hero} shares a deep bond with {beloved} while facing great emotional challenges.\n"
                "The drama begins with {problem},\n"
                "exacerbated by {obstacle}.\n"
                "Emotions intensify as {complication} develops,\n"
                "leading to a painful {predicament}.\n"
                "A turning point arises during the crisis: {crisis}.\n"
                "The story ends with a profound conclusion where {climax}.\n"
            )
        }

        template = genre_templates.get(self.genre, genre_templates["Dramatic"])
        self.last_plot_description = template.format(
            locale=plot["Locale"].lower(),
            hero=plot["Hero"].lower(),
            beloved=plot["Beloved"].lower(),
            problem=plot["Problem"].lower(),
            obstacle=plot["Obstacle"].lower(),
            complication=plot["Complication"].lower(),
            predicament=plot["Predicament"].lower(),
            crisis=plot["Crisis"].lower(),
            climax=plot["Climax"].lower()
        )

        if save:
            self.save_plot_to_file(genre=self.genre)
        return plot

    # def generate_plot(self, save=False, genre=None):
    #     """Randomly select one element from each story category to form a plot."""
    #     if genre is not None:
    #         self.genre = genre
    #     # Choose random values for required plot components
    #     for category in self.category_mapping.keys():
    #         element = self.filter_by_genre(category, self.genre)
    #         self.chosen_elements_index.append(element[0])
    #
    #     res = self.load_original_data()
    #
    #     plot = {
    #         "Genre": self.genre,
    #         "Locale": res[0],
    #         "Hero": res[1],
    #         "Beloved": res[2],
    #         "Problem": res[3],
    #         "Obstacle": res[4],
    #         "Complication": res[5],
    #         "Predicament": res[6],
    #         "Crisis": res[7],
    #         "Climax": res[8],
    #     }
    #
    #     # TODO: change the description - not always love.
    #     self.last_plot_description = (
    #         f"In this story set {plot['Locale'].lower()}, our hero is a {plot['Hero'].lower()} who falls in love with a {plot['Beloved'].lower()}...\n"
    #         f"Their goal is blocked by a major problem: {plot['Problem'].lower()}.\n"
    #         f"However, love does not come easy because {plot['Obstacle'].lower()}.\n"
    #         f"Things become more tangled when {plot['Complication'].lower()},\n"
    #         f"and matters worsen as {plot['Predicament'].lower()}.\n"
    #         f"At the height of tension, a crisis hits: {plot['Crisis'].lower()}.\n"
    #         f"The story climaxes in a twist where {plot['Climax'].lower()}\n"
    #     )
    #
    #     # Optionally save the generated plot to a new text file
    #     if save:
    #         self.save_plot_to_file(genre=self.genre)
    #     return plot

    def describe_plot(self):
        """
        Returns the formatted story skeleton as a readable text.

        Returns:
            str: Human-readable plot outline.
        """
        header = "📖 Here is your generated plot:\n" + "=" * 35 + "\n"
        return header + getattr(self, 'last_plot_description', "No plot generated yet.")

    def generate_adaptive_prompt(self, word_count, generate_plot=False, save=False, genre=None):
        """
        Constructs a detailed AI prompt for generating a full story based on a plot.

        Args:
            word_count (int): Target length for the final story.
            generate_plot (bool): Whether to generate a new plot or use the existing one.
            save (bool): Whether to save the prompt as a .txt file.
            genre (str): Specific genre to use (overrides default/random).

        Returns:
            str: Fully formatted prompt for use with a generative AI model.
        """

        if genre is not None:
            self.genre = genre
        else:
            self.genre = random.choice(self.genres)

        if generate_plot:
            self.generate_plot(save, self.genre)
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

        # Extract genre from plot if available
        # genre_emphasis = f"The story must reflect the conventions, tone, and structure of the '{self.genre}' genre." if self.genre else ""
        genre_emphasis = (
            f"GENRE FOCUS:\n"
            f"- The story must unmistakably reflect the '{self.genre}' genre.\n"
            f"- Include classic elements, tone, and structure from the genre.\n"
            f"- For example, if it's 'Comedy': use irony, misunderstandings, exaggeration, or wit.\n"
            if self.genre else ""
        )
        prompt = (
            f"Write a story of approximately {word_count} words.\n"
            f"{title_request}\n"
            f"{language_request}\n"
            f"The story is based on the following plot skeleton:\n"
            f"{plot_text}"
            f"{genre_emphasis}"
            f"Use the plot above to craft a complete narrative with the following guidelines:\n"
            f"{instructions}"
            f"- Describe the setting and emotional tone.\n"
            f"- Emphasize the central conflict.\n"
            f"- Use natural dialogue where appropriate.\n"
            f"- You may expand on events while remaining faithful to the plot.\n"
            f"Aim for a smooth and engaging narrative voice. A dramatic or open ending is welcome.\n"
            f"{advanced_criteria}"
        )

        if save:
            save_prompt_to_file(prompt, genre=self.genre)

        return prompt

    def check_genre_filter_coverage(self, genre=None, threshold=0.2):
        """
        Diagnoses how well the selected genre filters the dataset by counting how many
        items pass the cosine similarity threshold per category.

        Args:
            genre (str): Genre to check.
            threshold (float): Cosine similarity threshold.

        Returns:
            dict: Coverage report per category (items matched / total).
        """
        if genre is None:
            genre = self.genre

        genre_embedding = self.genre_embeddings.get(genre)
        if genre_embedding is None:
            print(f"⚠️ No embedding found for genre: {genre}")
            return {}

        coverage = {}
        for category in self.category_mapping:
            if category not in self.embeddings_cache:
                continue

            candidates = self.embeddings_cache[category]
            count = 0

            for item in candidates:
                similarity = util.cos_sim(genre_embedding, item["embedding"]).item()
                if similarity >= threshold:
                    count += 1

            total = len(candidates)
            print(f"📂 {category.capitalize()}: {count}/{total} items above threshold {threshold}")
            coverage[category] = (count, total)

        return coverage

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
        """
        Saves the last plot description to a numbered file. If genre is provided,
        it appends it to the filename for easier organization.

        Args:
            genre (str, optional): Genre string to include in the filename.
        """
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
