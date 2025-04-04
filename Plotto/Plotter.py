import abc

# from graphviz import Digraph
import re
from typing import List, Dict, Optional
# from utils import random_clause, random_name
import random
import logging

class Plotter(abc.ABC):
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
       pass

    def generate(self, lead_ins: int = 1, carry_ons: int = 1):
       pass

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
       pass

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

