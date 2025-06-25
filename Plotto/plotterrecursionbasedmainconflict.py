# from graphviz import Digraph
import os

import re
from typing import List, Dict, Optional
import random
import logging

from Plotto.helper_funcs import random_clause, random_name

logging.basicConfig(level=logging.DEBUG)

def save_prompt_to_file(prompt):
    """
    Saves a generated AI prompt to a uniquely numbered text file.

    Args:
        prompt (str): The prompt string to be saved.
    """
    directory = "Results/Plotto_Prompts"
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

class PlotterRecursionBasedMainConflict:
    """A class for generating plots based on predefined data and templates."""

    def __init__(self, plotto_data, gender_map, pronoun_map, flip_genders=False, names_data=None):
        """Initialize the Plotter class."""
        # super().__init__( plotto_data, gender_map, pronoun_map, flip_genders=False, names_data=None)
        self.plotto = plotto_data
        self.gender_map = gender_map  # Add gender_map as an instance variable
        self.pronoun_map = pronoun_map  # Add pronoun map as an instance variable
        self.flip_genders = flip_genders
        self.expand_ids = []  # Store all expand IDs
        self.ordered_sentences = []  # Track sentences in the order they appear
        # self.graph = Digraph(format="png")  # Initialize Graphviz graph
        self.names_data = names_data or {"male_names": [], "female_names": []}
        self.pronoun_pattern = re.compile(r'\b(' + '|'.join(self.pronoun_map.keys()) + r')\b')
        self.root = None
        self.lead_ins = 0
        self.carry_ons = 0
        self.curr_name_mapping = {}
        self.transforms_dict = {}

    def _picker(self, items: List, label: Optional[str] = None) -> Optional[str]:
        """Randomly pick an item from a list."""
        if not items:
            if label:
                logging.debug(f"No items to pick from for label: {label}")
            return None
        return random.choice(items)

    def generate_graph(self, ordered_sentences: List[str], plot: Dict[str, str]):
        """Generate a graph based on the ordered sentences."""
        self.graph.attr(rankdir="TB")
        previous_node = None
        for sentence_id in ordered_sentences:
            if sentence_id == plot["description"]:
                current_node = "node_B_clause"
                self.graph.node(
                    current_node,
                    f"B clause: {plot['description']}",
                    shape="box",
                    style="rounded,filled",
                    color="lightgreen",
                )
            elif sentence_id == plot["c clause"]:
                current_node = "node_C_clause"
                self.graph.node(current_node, f"C clause: {plot['c clause']}", shape="box", style="rounded,filled",
                                color="lightgreen", )
            else:
                # Handle regular sentences
                current_node = None
                for sentence in plot["plot"].split("\n"):
                    if f"[{sentence_id}]" in sentence:
                        current_node = f"node_{sentence_id}"
                        self.graph.node(
                            current_node,
                            sentence.strip(),
                            shape="box",
                            style="rounded,filled",
                            color="lightblue",
                        )
                        break
            # Add an edge from the previous node to the current node, if any
            if current_node and previous_node:
                self.graph.edge(previous_node, current_node)
            # Update previous_node
            if current_node:
                previous_node = current_node
        # Render the graph to a file
        self.graph.render("Plot Based Main Conflict Recursion", view=True)

    def generate(self, lead_ins: int = 1, carry_ons: int = 1):
        """Generate a plot and construct a graph."""
        self.carry_ons = carry_ons
        self.lead_ins = lead_ins
        flip = self.flip_genders
        if flip is None:
            flip = random.choice([True, False])
        root_transform = {}
        A_Clause = random_clause(self.plotto['A_Clauses'])
        B_Clause = random_clause(self.plotto['B_Clauses'])
        logging.debug(f"B_Clause: {B_Clause}")
        C_Clause = random_clause(self.plotto['C_Clauses'])
        root_id = "root"
        conflict = self.plotto['conflicts'][random_clause(B_Clause['nodes'])]
        logging.debug(f"Selected conflict ID: {conflict}")
        # actors = []
        self.root = conflict
        plot = self._expand(conflict, root_transform, {"leadIns": self.lead_ins, "carryOns": self.carry_ons},
                            expand_id=root_id).replace('*', '')
        plot = self._apply_names(plot)
        plot = self.fix_pronouns_contextually(plot, self.curr_name_mapping)
        return {
                "a clause": f"{A_Clause}",
                "group": B_Clause["group"],
                "subgroup": B_Clause["subgroup"],
                "description": B_Clause["description"],
                "actors": [{"symbol": symbol, "name": name} for symbol, name in self.curr_name_mapping.items()],
                "main conflict": conflict["description"],
                "plot": f"{B_Clause}\n\n{plot}\n\n{C_Clause}".strip(),
                "c clause": f"{C_Clause}"
                }

    def generate_prompt(self, plot_string, word_count, save=True):
        prompt = f""" 
                  Role: you are story writing expert
                  The Plot:
                  {plot_string}

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
                                      write the title of the story at the beginning of the story, in the next format: the real title of the story
                  """

        if save:
            save_prompt_to_file(prompt)

        return prompt
    #### need to check the purpose of this function ####
    def _get_gender_transform(self):
        """Create a mapping to flip genders."""
        transform = {f"A-{i}": f"B-{i}" for i in range(10)}
        transform.update({f"B-{i}": f"A-{i}" for i in range(10)})
        return transform

    #re-write the function
    def _apply_names(self, text: str) -> str:
        """Replace character symbols with names, treating suffixes as distinct characters."""
        if isinstance(text, list):
            text = text[0]
        male_names = self.names_data["male_names"]
        female_names = self.names_data["female_names"]
        rg = self._transform_to_regex(self.plotto['characters'])
        if rg:
            def replacer(match):
                symbol = match.group(0)  # Full match, e.g., "A-2"
                if symbol in self.curr_name_mapping:
                    return self.curr_name_mapping[symbol]
                description = self.plotto['characters'].get(symbol, '')
                gender = self.gender_map.get(symbol, 'any')
                name = random_name(symbol, gender, male_names, female_names)
                self.curr_name_mapping[symbol] = name
                # actors.append({"symbol": symbol, "name": name, "description": description})
                return name
            return re.sub(rg, replacer, text)
        return text

    #re-write the function
    def _transform_to_regex(self, mapping: dict) -> re.Pattern:
        """Create a regex pattern for matching character symbols."""
        keys = [str(key) for key in sorted(mapping.keys(), key=len, reverse=True)]
        if not keys:
            return re.compile(r'(?!x)x')  # Matches nothing
        # Match exact words and variants like `A-2` or `A_b`
        pattern = r'\b(?:' + '|'.join(map(re.escape, keys)) + r')\b(?:(?:-|\b)\w+)?'
        return re.compile(pattern)

    def fill_sentences(self, sentence_id):
            full_sentence = ''
            new_description = self.plotto['conflicts'][sentence_id]['description']
            if isinstance(new_description, list):
                for s_id in new_description:
                    full_sentence += ', ' + self.fill_sentences(s_id)
                return full_sentence
            else:
                return new_description

    # def tfm_characters(self, tfm, sentence):
    #     print(f'characters are: {self.curr_name_mapping.items()}')
    #     for org, new in tfm.items():
    #         self.known_symbols(org)
    #         self.known_symbols(new)
    #         print(f'tfm items: {tfm.items()}')
    #         original_character = self.curr_name_mapping.get(org)
    #         new_character = self.curr_name_mapping.get(new)
    #         # if not new_character:
    #         #     new_character = utils.random_name(new, self.gender_map[new], self.names_data["male_names"],
    #         #                                       self.names_data["female_names"])
    #         #     self.curr_name_mapping[new] = new_character
    #         # if not original_character:
    #         #     original_character = utils.random_name(new, self.gender_map[org], self.names_data["male_names"],
    #         #                                            self.names_data["female_names"])
    #         #     self.curr_name_mapping[org] = original_character
    #         print(f'original character: {original_character}')
    #         print(f'new character: {new_character}')
    #         sentence = sentence.replace(original_character, new_character)
    #     return sentence

    import re

    def tfm_characters(self, tfm, sentence):
        all_sentences = sentence.split("\n\n")
        curr_sentence = all_sentences[0]
        # Split the current sentence by spaces, commas, periods, single quotes, and other punctuation marks
        # This updated regex ensures apostrophes are correctly handled as delimiters
        words = re.split(r'(\s+|[.,!?;()]+)', curr_sentence)
        transformed_words = []
        for word in words:
            if word.endswith("’s") or word.endswith("'s"):
                base = word[:-2]
                suffix = word[-2:]
                if base in tfm:
                    transformed_words.append(tfm[base] + suffix)
                else:
                    transformed_words.append(word)
            elif word in tfm:
                new_word = tfm[word]
                # Check for circular transformation (new_word -> word)
                # if new_word in tfm and tfm.get(new_word) == word:
                #     # Circular transformation detected, skip transformation for this word
                #     transformed_words.append(word)
                # else:
                transformed_words.append(new_word)  # Apply the transformation if no circular reference
            else:
                transformed_words.append(word)  # Keep the word as is if no transformation
        # Join the transformed words back into a sentence
        all_sentences[0] =  "".join(transformed_words)
        return "\n\n".join(all_sentences)

    def known_symbols(self, symbol):
        if self.curr_name_mapping.get(symbol) is None:
            if self.gender_map.get(symbol):
                gender = self.gender_map.get(symbol)
                male_names = self.names_data["male_names"]
                female_names = self.names_data["female_names"]
                name = random_name(symbol, gender, male_names, female_names)
                self.curr_name_mapping[symbol] = name

    def _expand(self, item, transform, ctx, start=None, end=None, expand_id="", visited_ids=None):
        """Expand an item recursively and track meaningful IDs in order."""
        if visited_ids is None:
            visited_ids = set()

        self.expand_ids.append(expand_id)
        ret = []
        if not item:
            return f'NULL [{expand_id}]'

        # Add the main conflict description if it hasn't been added yet
        if isinstance(item, dict) and "conflictid" in item:
            sentence_id = item.get("conflictid")
            if sentence_id not in self.ordered_sentences:
                if ctx["leadIns"] == 0 and len(self.ordered_sentences) == self.lead_ins + 1:
                    self.root = item
                    self.ordered_sentences = list(reversed(self.ordered_sentences))
                self.ordered_sentences.append(sentence_id)


                description = item.get('description', '')
                if isinstance(description, list):
                    expanded_description = []
                    for part in description:
                        if isinstance(part, str):
                            expanded_description.append(part)
                        elif isinstance(part, list):
                            for sub_part in part:
                                if isinstance(sub_part, str):
                                    expanded_description.append(self.expand_inner_conflict(sub_part, transform, visited_ids=visited_ids))
                                elif isinstance(sub_part, dict):
                                    sub_v = sub_part.get("v")
                                    sub_transform = sub_part.get("tfm", {})
                                    start = sub_part.get("start", "")
                                    end = sub_part.get("end", "")
                                    if isinstance(sub_v, list):
                                        if "op" in sub_part:
                                            operation = sub_part["op"]
                                            if operation == "+":
                                                for sub_v_item in sub_v:
                                                    expanded_description.append(
                                                        self.expand_inner_conflict(sub_v_item, sub_transform, start,
                                                                                   end, visited_ids=visited_ids)
                                                    )
                                            elif operation == "?":
                                                selected_value = self._picker(sub_v, "plot option")
                                                if isinstance(selected_value, dict):
                                                    selected_id = selected_value.get("v")
                                                    selected_tfm = selected_value.get("tfm", {})
                                                    selected_start = selected_value.get("start", "")
                                                    selected_end = selected_value.get("end", "")
                                                    expanded_description.append(
                                                        self.expand_inner_conflict(selected_id, selected_tfm,
                                                                                   selected_start, selected_end, visited_ids=visited_ids)
                                                    )
                                                else:
                                                    expanded_description.append(
                                                        self.expand_inner_conflict(selected_value, sub_transform, start,
                                                                                   end, visited_ids=visited_ids)
                                                    )
                                        else:
                                            for sub_v_item in sub_v:
                                                expanded_description.append(
                                                    self.expand_inner_conflict(sub_v_item, sub_transform, start, end, visited_ids=visited_ids)
                                                )
                                    elif isinstance(sub_v, str):
                                        expanded_description.append(
                                            self.expand_inner_conflict(sub_v, sub_transform, start, end, visited_ids=visited_ids)
                                        )
                        elif isinstance(part, dict):
                            sub_v = part.get("v")
                            sub_transform = part.get("tfm", {})
                            start = part.get("start", "")
                            end = part.get("end", "")
                            if isinstance(sub_v, list):
                                if "op" in part:
                                    operation = part["op"]
                                    if operation == "+":
                                        for sub_v_item in sub_v:
                                            if isinstance(sub_v_item, dict):
                                                inner_id = sub_v_item.get("v")
                                                inner_tfm = sub_v_item.get("tfm", {})
                                                inner_start = sub_v_item.get("start", "")
                                                inner_end = sub_v_item.get("end", "")
                                                expanded_description.append(
                                                    self.expand_inner_conflict(inner_id, inner_tfm, inner_start,
                                                                               inner_end, visited_ids=visited_ids)
                                                )
                                            else:
                                                expanded_description.append(
                                                    self.expand_inner_conflict(sub_v_item, sub_transform, start, end, visited_ids=visited_ids)
                                                )

                                    elif operation == "?":
                                        selected_value = self._picker(sub_v, "plot option")
                                        if isinstance(selected_value, dict):
                                            selected_id = selected_value.get("v")
                                            selected_tfm = selected_value.get("tfm", {})
                                            selected_start = selected_value.get("start", "")
                                            selected_end = selected_value.get("end", "")
                                            expanded_description.append(
                                                self.expand_inner_conflict(selected_id, selected_tfm, selected_start,
                                                                           selected_end, visited_ids=visited_ids)
                                            )
                                        else:
                                            expanded_description.append(
                                                self.expand_inner_conflict(selected_value, sub_transform, start, end, visited_ids=visited_ids)
                                            )
                                else:
                                    for sub_v_item in sub_v:
                                        expanded_description.append(
                                            self.expand_inner_conflict(sub_v_item, sub_transform, start, end, visited_ids=visited_ids)
                                        )
                            elif isinstance(sub_v, str):
                                expanded_description.append(
                                    self.expand_inner_conflict(sub_v, sub_transform, start, end, visited_ids=visited_ids)
                                )
                    item['description'] = ''.join(expanded_description)

                ret.append(f"{item['description']} [{sentence_id}]")

        if ctx.get("leadIns", 0) > 0 and "leadIns" in item:
            ctx["leadIns"] -= 1
            lead_in_id = f"{expand_id}-leadIn"
            lead_in_result = self._expand(item["leadIns"], None, ctx, expand_id=lead_in_id)
            ret.append(lead_in_result)

        if ctx.get("carryOns", 0) > 0 and "carryOns" in item:
            ctx["carryOns"] -= 1
            carryon_id = f"{expand_id}-carryOn"
            carryon = self._expand(self.root["carryOns"], transform, ctx, expand_id=carryon_id)
            ret.append(carryon)

        if isinstance(item, str):
            expanded_item = self._expand(self.plotto["conflicts"].get(item, None), None, ctx,
                                         expand_id=f"{expand_id}-str")
            ret.append(expanded_item)
        elif isinstance(item, list):
            expanded_list = self._expand(self._picker(item, "plot option"), None, ctx, expand_id=f"{expand_id}-list")
            ret.append(expanded_list)
        elif "v" in item:
            if isinstance(item['v'], str):
                if self.transforms_dict.get(item['v']) is None and item.get('tfm') and self.gender_map.get(
                        list(item.get('tfm').keys())[0]):
                    self.transforms_dict[item['v']] = item.get("tfm")
            if item.get("start") or item.get("end"):
                expanded_v = self._expand(
                    self.plotto["conflicts"].get(item["v"], None),
                    item.get("tfm"),
                    ctx,
                    item.get("start"),
                    item.get("end"),
                    expand_id=f"{expand_id}-vstartend"
                )
                if item.get("tfm"):
                    expanded_v = self.tfm_characters(item.get("tfm"), expanded_v)
                ret.append(expanded_v)
            elif item.get("op") == "+":
                for sub in item["v"]:
                    expanded_sub = self._expand(sub, item.get("tfm"), ctx, expand_id=f"{expand_id}-vop")
                    if item.get("tfm"):
                        expanded_sub = self.tfm_characters(item.get("tfm"), expanded_sub)
                    ret.append(expanded_sub)
            else:
                expanded_v = self._expand(item["v"], item.get("tfm"), ctx, expand_id=f"{expand_id}-v")
                if item.get("tfm"):
                    expanded_v = self.tfm_characters(item.get("tfm"), expanded_v)
                ret.append(expanded_v)

        result = "\n\n".join(ret).strip()
        return result

    def fix_pronouns_contextually(self, text: str, actors: dict) -> str:
        name_to_gender = {actor[1]: self.gender_map.get(actor[0], "none") for actor in actors.items()}

        def replace_pronoun_with_context(match):
            pronoun = match.group(0)
            preceding_text = match.string[:match.start()]
            for name, gender in name_to_gender.items():
                if name in preceding_text:
                    return self.pronoun_map.get(pronoun, {}).get(gender, pronoun)
            return pronoun

        return self.pronoun_pattern.sub(replace_pronoun_with_context, text)

    def expand_inner_conflict(self, conflict_id, transform=None, start=None, end=None, visited_ids=None):
        """
        Expand a specific conflict, apply transformations if needed,
        and return the expanded description.
        """
        if visited_ids is None:
            visited_ids = set()

        while isinstance(conflict_id, dict):
            transform = conflict_id.get("tfm", transform)
            start = conflict_id.get("start", start)
            end = conflict_id.get("end", end)
            conflict_id = conflict_id.get("v")

        while isinstance(conflict_id, list):
            conflict_id = random.choice(conflict_id)
            if isinstance(conflict_id, dict):
                transform = conflict_id.get("tfm", transform)
                start = conflict_id.get("start", start)
                end = conflict_id.get("end", end)
                conflict_id = conflict_id.get("v")

        if conflict_id in visited_ids:
            return f"[Conflict {conflict_id} – recursion stopped to prevent infinite loop]"

        visited_ids.add(conflict_id)

        conflict = self.plotto["conflicts"].get(conflict_id, None)
        if not conflict:
            return f"[Conflict {conflict_id} not found]"

        description = conflict.get("description", "")
        if isinstance(description, str):
            if start or end:
                start = start or ""
                end = end or ""
                description = f"{start}{description}{end}"
            if transform:
                description = self.tfm_characters(transform, description)
            return description

        elif isinstance(description, list):
            expanded_description = []
            for part in description:
                if isinstance(part, str):
                    expanded_description.append(part)
                elif isinstance(part, list):
                    for sub_conflict_id in part:
                        if isinstance(sub_conflict_id, dict):
                            inner_id = sub_conflict_id.get("v")
                            inner_tfm = sub_conflict_id.get("tfm", {})
                            inner_start = sub_conflict_id.get("start", "")
                            inner_end = sub_conflict_id.get("end", "")
                            expanded_sub_description = self.expand_inner_conflict(
                                inner_id, inner_tfm, inner_start, inner_end, visited_ids=visited_ids
                            )
                        else:
                            expanded_sub_description = self.expand_inner_conflict(sub_conflict_id, transform, visited_ids=visited_ids)
                        expanded_description.append(expanded_sub_description)
                elif isinstance(part, dict):
                    inner_id = part.get("v")
                    inner_tfm = part.get("tfm", {})
                    inner_start = part.get("start", "")
                    inner_end = part.get("end", "")
                    expanded_sub_description = self.expand_inner_conflict(
                        inner_id, inner_tfm, inner_start, inner_end, visited_ids=visited_ids
                    )
                    expanded_description.append(expanded_sub_description)
            return ''.join(expanded_description)
