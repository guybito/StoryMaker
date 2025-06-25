import abc
import logging
import random
import re
from typing import List, Optional, Dict, Any

from Plotto.helper_funcs import random_name


class Plotter(abc.ABC):
    """
    Abstract base class for plot generation and manipulation using Plotto data.
    """

    def __init__(
            self,
            plotto_data: Dict[str, Any],
            gender_map: Dict[str, str],
            pronoun_map: Dict[str, Dict[str, str]],
            flip_genders: bool = False,
            names_data: Optional[Dict[str, List[str]]] = None
    ):
        """
        Initialize the Plotter class.

        :param plotto_data: The main Plotto data structure.
        :param gender_map: Mapping of character symbols to gender.
        :param pronoun_map: Mapping of pronouns to their gendered forms.
        :param flip_genders: If True, will flip genders in transformation.
        :param names_data: Optional dictionary of names by gender.
        """
        self.plotto = plotto_data
        self.gender_map = gender_map
        self.pronoun_map = pronoun_map
        self.flip_genders = flip_genders
        self.expand_ids: List[str] = []
        self.ordered_sentences: List[str] = []
        self.names_data = names_data or {"male_names": [], "female_names": []}
        self.pronoun_pattern = re.compile(r'\b(' + '|'.join(self.pronoun_map.keys()) + r')\b')
        self.lead_ins = 0
        self.carry_ons = 0
        self.curr_name_mapping: Dict[str, str] = {}
        self.transforms_dict: Dict[str, str] = {}

    def _picker(self, items: List[Any], label: Optional[str] = None) -> Optional[Any]:
        """
        Randomly select an item from a list.
        :param items: List of items to choose from.
        :param label: Optional label for debugging/logging purposes.
        :return: Selected item or None if the list is empty.
        """
        if not items:
            if label:
                logging.debug(f"No items to pick from for label: {label}")
            return None
        return random.choice(items)

    def _get_gender_transform(self) -> Dict[str, str]:
        """
        Create a mapping to flip genders between symbols A-* and B-*.
        :return: Dictionary mapping symbols to their flipped counterpart.
        """
        transform = {f"A-{i}": f"B-{i}" for i in range(10)}
        transform.update({f"B-{i}": f"A-{i}" for i in range(10)})
        return transform

    def _apply_names(self, text: str) -> str:
        """
        Replace character symbols with names, treating suffixes as distinct characters.
        :param text: The text in which to replace symbols.
        :return: Text with character symbols replaced by names.
        """
        if isinstance(text, list):
            text = text[0]
        male_names = self.names_data["male_names"]
        female_names = self.names_data["female_names"]
        regex = self._transform_to_regex(self.plotto['characters'])
        if regex:
            def replacer(match):
                symbol = match.group(0)
                if symbol in self.curr_name_mapping:
                    return self.curr_name_mapping[symbol]
                gender = self.gender_map.get(symbol, 'any')
                name = random_name(symbol, gender, male_names, female_names)
                self.curr_name_mapping[symbol] = name
                return name

            return regex.sub(replacer, text)
        return text

    def _transform_to_regex(self, mapping: dict) -> Optional[re.Pattern]:
        """
        Create a regex pattern for matching character symbols.
        :param mapping: Dictionary whose keys are symbols to match.
        :return: Compiled regex pattern or None if mapping is empty.
        """
        keys = [str(key) for key in sorted(mapping.keys(), key=len, reverse=True)]
        if not keys:
            return re.compile(r'(?!x)x')  # Matches nothing
        pattern = r'\b(?:' + '|'.join(map(re.escape, keys)) + r')\b(?:(?:-|\b)\w+)?'
        return re.compile(pattern)

    def fill_sentences(self, sentence_id: str) -> str:
        """
        Recursively fill and concatenate sentences by sentence_id.
        :param sentence_id: The ID of the sentence or group of sentences.
        :return: Concatenated string of sentences.
        """
        full_sentence = ''
        new_description = self.plotto['conflicts'][sentence_id]['description']
        if isinstance(new_description, list):
            for s_id in new_description:
                full_sentence += ', ' + self.fill_sentences(s_id)
            return full_sentence
        else:
            return new_description

    def tfm_characters(self, tfm: Dict[str, str], sentence: str) -> str:
        """
        Transform characters in the sentence according to the mapping.
        :param tfm: Transformation dictionary from original to new symbols.
        :param sentence: The sentence in which to transform characters.
        :return: Sentence with transformed character names.
        """
        for org, new in tfm.items():
            self.known_symbols(new)
            original_character = self.curr_name_mapping.get(org)
            new_character = self.curr_name_mapping.get(new)
            if original_character and new_character:
                sentence = sentence.replace(original_character, new_character)
        return sentence

    def known_symbols(self, symbol: str) -> None:
        """
        Ensure that the symbol has a mapped name in the current mapping.
        :param symbol: The character symbol to check/add.
        """
        if self.curr_name_mapping.get(symbol) is None:
            if self.gender_map.get(symbol):
                gender = self.gender_map[symbol]
                male_names = self.names_data["male_names"]
                female_names = self.names_data["female_names"]
                name = random_name(symbol, gender, male_names, female_names)
                self.curr_name_mapping[symbol] = name

    def _expand(self, item, transform, ctx, start=None, end=None, expand_id=""):
        """
        Abstract method for expanding plot items.
        To be implemented by subclasses.
        """
        pass

    def fix_pronouns_contextually(self, text: str, actors: Dict[str, str]) -> str:
        """
        Fix pronouns in the text based on the provided actors and their genders.
        :param text: The input text to fix.
        :param actors: Dictionary mapping symbols to actor names.
        :return: Text with contextually fixed pronouns.
        """
        name_to_gender = {actor[1]: self.gender_map.get(actor[0], "none") for actor in actors.items()}

        def replace_pronoun_with_context(match):
            pronoun = match.group(0)
            preceding_text = match.string[:match.start()]
            for name, gender in name_to_gender.items():
                if name in preceding_text:
                    return self.pronoun_map.get(pronoun, {}).get(gender, pronoun)
            return pronoun

        return self.pronoun_pattern.sub(replace_pronoun_with_context, text)
