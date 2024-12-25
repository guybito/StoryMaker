import random
import json
from typing import List, Dict


def load_names(file_path: str) -> Dict[str, List[str]]:
    """Load male and female names from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_gender_map(file_path: str) -> Dict[str, str]:
    """Load the gender map from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_pronoun_map(file_path: str) -> Dict[str, Dict[str, str]]:
    """Load the pronoun map from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

# function to pick random caluse
def random_clause(arr):
    """Select a random clause from a list.
    Parameters:arr (list): A list of items to choose from.
    Returns:Any: A randomly selected item from the list, or None if the list is empty."""
    if not arr:
        return None
    return random.choice(arr)

def random_name(character_symbol: str, gender: str,
                 male_names: List[str], female_names: List[str]) -> str:
    """Generate a random name based on gender."""
    if gender == 'male':
        names = male_names
    elif gender == 'female':
        names = female_names
    elif gender == 'any':
        names = male_names if random.random() < 0.5 else female_names
    else:
        return character_symbol

    if names:
        name = names.pop(random.randint(0, len(names) - 1))
        return name
    return character_symbol


