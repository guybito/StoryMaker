from graphviz import Digraph
import re
from typing import List, Dict, Optional
from utils import random_clause, random_name
import random
import logging

logging.basicConfig(level=logging.DEBUG)


class PlotterRecursionBasedLeadIns:
    """A class for generating plots based on predefined data and templates."""

    def __init__(self, plotto_data, gender_map, pronoun_map, flip_genders=False, names_data=None):
        """Initialize the Plotter class."""
        self.plotto = plotto_data
        self.gender_map = gender_map  # Add gender_map as an instance variable
        self.pronoun_map = pronoun_map  # Add pronoun map as an instance variable
        self.flip_genders = flip_genders
        self.expand_ids = []  # Store all expand IDs
        self.ordered_sentences = []  # Track sentences in the order they appear
        self.graph = Digraph(format="png")  # Initialize Graphviz graph
        self.names_data = names_data or {"male_names": [], "female_names": []}
        self.pronoun_pattern = re.compile(r'\b(' + '|'.join(self.pronoun_map.keys()) + r')\b')
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
        self.graph.render("Plot Based Lead Ins Recursion", view=True)

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
        # self.root = conflict
        plot = self._expand(conflict, root_transform, {"leadIns": self.lead_ins, "carryOns": self.carry_ons},
                            expand_id=root_id).replace('*', '')
        plot = self.fix_pronouns_contextually(plot, self.curr_name_mapping)
        return {
                "a clause": f"{A_Clause}",
                "group": B_Clause["group"],
                "subgroup": B_Clause["subgroup"],
                "description": B_Clause["description"],
                "actors": [{"symbol": symbol, "name": name} for symbol, name in self.curr_name_mapping.items()],
                "plot": f"{B_Clause}\n\n{plot}\n\n{C_Clause}".strip(),
                "c clause": f"{C_Clause}"
                }
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

    # def _transform_to_regex(self, mapping: dict) -> re.Pattern:
    #     """Create a regex pattern for matching character symbols."""
    #     keys = [str(key) for key in sorted(mapping.keys(), key=len, reverse=True)]
    #     if not keys:
    #         return re.compile(r'(?!x)x')  # Matches nothing
    #     # pattern = r'\b(?:' + '|'.join(map(re.escape, keys)) + r')(?![a-z])'
    #     pattern = r'\b(?:' + '|'.join(map(re.escape, keys)) + r')\b(?![a-z])'
    #     return re.compile(pattern)

    def fill_sentences(self, sentence_id):
            full_sentence = ''
            new_description = self.plotto['conflicts'][sentence_id]['description']
            if isinstance(new_description, list):
                for s_id in new_description:
                    full_sentence += ', ' + self.fill_sentences(s_id)
                return full_sentence
            else:
                return new_description

    def tfm_characters(self, tfm, sentence):
        print(f'characters are: {self.curr_name_mapping.items()}')
        for org, new in tfm.items():
            self.known_symbols(new)
            print(f'tfm items: {tfm.items()}')
            original_character = self.curr_name_mapping.get(org)
            new_character = self.curr_name_mapping.get(new)
            print(f'original character: {original_character}')
            print(f'new character: {new_character}')
            sentence = sentence.replace(original_character, new_character)
        return sentence

    def known_symbols(self, symbol):
        if self.curr_name_mapping.get(symbol) is None:
            if self.gender_map.get(symbol):
                gender = self.gender_map.get(symbol)
                male_names = self.names_data["male_names"]
                female_names = self.names_data["female_names"]
                name = random_name(symbol, gender, male_names, female_names)
                self.curr_name_mapping[symbol] = name


    def _expand(self, item, transform, ctx, start=None, end=None, expand_id=""):
        """Expand an item recursively and track meaningful IDs in order."""
        self.expand_ids.append(expand_id)
        ret = []
        if not item:
            return f'NULL [{expand_id}]'
        # Add the main conflict description if it hasn't been added yet
        if isinstance(item, dict) and "conflictid" in item:
            sentence_id = item.get("conflictid")
            if sentence_id not in self.ordered_sentences:
                # if ctx["leadIns"] == 0 and len(self.ordered_sentences) == self.lead_ins + 1:
                    # self.root = item
                    # self.ordered_sentences = list(reversed(self.ordered_sentences))
                self.ordered_sentences.append(sentence_id)
                # Track the sentence order
                print("description")
                print(item['description'])
                # if isinstance(item['description'], list):
                #     rest_of_sentence = ''
                #     curr_sentence_description = item['description'][0]
                #     for s_id in item['description'][1]:
                #         rest_of_sentence += self.fill_sentences(s_id)
                #     item["description"] = curr_sentence_description + rest_of_sentence
                # item['description'] = self._apply_names(item['description'])
                item['description'] = self._apply_names(item['description'])
                ret.append(f"{item['description']} [{sentence_id}]")
                logging.debug(f"Added main conflict to plot: {sentence_id}")

        if ctx.get("leadIns", 0) > 0 and "leadIns" in item:
            ctx["leadIns"] -= 1
            lead_in_id = f"{expand_id}-leadIn"
            logging.debug(f"Processing lead-in for main conflict: {item.get('conflictid', 'N/A')}")
            lead_in_result = self._expand(item["leadIns"], None, ctx, expand_id=lead_in_id)
            # Apply names to the lead-in result
            lead_in_result = self._apply_names(lead_in_result)
            ret.append(lead_in_result)
        # Handle carry-ons
        if ctx.get("carryOns", 0) > 0 and "carryOns" in item:
            ctx["carryOns"] -= 1
            carryon_id = f"{expand_id}-carryOn"
            logging.debug(f"Processing carry-on for main conflict: {item.get('conflictid', 'N/A')}")
            carryon = self._expand(item["carryOns"], transform, ctx, expand_id=carryon_id)
            # Apply names to the carry-on result
            carryon = self._apply_names(carryon)
            ret.append(carryon)
        # Expand sub-items
        if isinstance(item, str):
            logging.debug(f"Expanding conflict: {item}")
            expanded_item = self._expand(self.plotto["conflicts"].get(item, None), None, ctx,
                                         expand_id=f"{expand_id}-str")
            # Apply names to the expanded string item
            expanded_item = self._apply_names(expanded_item)
            ret.append(expanded_item)
        elif isinstance(item, list):
            logging.debug(f"Expanding conflict list: {item}")
            expanded_list = self._expand(self._picker(item, "plot option"), None, ctx, expand_id=f"{expand_id}-list")
            # Apply names to the expanded list item
            expanded_list = self._apply_names(expanded_list)
            ret.append(expanded_list)
        elif "v" in item:
            if isinstance(item['v'], str):
                if self.transforms_dict.get(item['v']) is None and item.get('tfm') and self.gender_map.get(list(item.get('tfm').keys())[0]):
                    self.transforms_dict[item['v']] = item.get("tfm")
            if item.get("start") or item.get("end"):
                logging.debug(f"Expanding conflict v with start or end options: {item}")
                expanded_v = self._expand(
                    self.plotto["conflicts"].get(item["v"], None),
                    item.get("tfm"),
                    ctx,
                    item.get("start"),
                    item.get("end"),
                    expand_id=f"{expand_id}-vstartend"
                )
                # Apply names to the expanded v item
                if item.get("tfm"):
                    expanded_v = self.tfm_characters(item.get("tfm"), expanded_v)
                expanded_v = self._apply_names(expanded_v)
                ret.append(expanded_v)
            elif item.get("op") == "+":
                logging.debug(f"Expanding conflict v with chaining: {item}")
                for sub in item["v"]:
                    expanded_sub = self._expand(sub, item.get("tfm"), ctx, expand_id=f"{expand_id}-vop")
                    # Apply names to each sub-item in the list
                    if item.get("tfm"):
                        expanded_sub = self.tfm_characters(item.get("tfm"), expanded_sub)
                    expanded_sub = self._apply_names(expanded_sub)
                    ret.append(expanded_sub)
            else:
                logging.debug(f"Expanding conflict v: {item}")
                expanded_v = self._expand(item["v"], item.get("tfm"), ctx, expand_id=f"{expand_id}-v")
                # Apply names to the expanded v item
                if item.get("tfm"):
                        expanded_v = self.tfm_characters(item.get("tfm"), expanded_v)
                expanded_v = self._apply_names(expanded_v)
                ret.append(expanded_v)
        # Combine results
        result = "\n\n".join(ret).strip()
        # Apply names to the final result
        result = self._apply_names(result)
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
