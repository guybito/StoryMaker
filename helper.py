import random
from typing import List, Dict, Optional
import re
import json

# Gender mapping
gender_map = {
    "A": "male", "A-2": "male", "A-3": "male", "A-4": "male", "A-5": "male", "A-6": "male",
    "A-7": "male", "A-8": "male", "A-9": "male", "B": "female", "B-2": "female", "B-3": "female",
    "B-4": "female", "B-5": "female", "B-6": "female", "B-7": "female", "B-8": "female",
    "B-9": "female", "F-A": "father", "M-A": "mother", "BR-A": "male", "SR-A": "female",
    "SN-A": "male", "D-A": "female", "U-A": "male", "AU-A": "female", "CN-A": "male",
    "NW-A": "male", "NC-A": "female", "GF-A": "male", "GM-A": "female", "SF-A": "male",
    "SM-A": "female", "GCH-A": "any", "F-B": "male", "M-B": "female", "BR-B": "male",
    "SR-B": "female", "SN-B": "male", "D-B": "female", "U-B": "male", "AU-B": "female",
    "CN-B": "female", "NW-B": "male", "NC-B": "female", "GF-B": "male", "GM-B": "female",
    "SF-B": "male", "SM-B": "female", "GCH-B": "any", "BR": "male", "SR": "female",
    "SN": "male", "D": "female", "CN": "any", "CH": "any", "AX": "male", "BX": "female", "X": "none"
}

# function to pick random caluse
def random_clause(arr):
    """Select a random clause from a list.
    Parameters:arr (list): A list of items to choose from.
    Returns:Any: A randomly selected item from the list, or None if the list is empty."""
    if not arr:
        return None
    return random.choice(arr)

def random_name(character_symbol: str, symbol_description: str, gender: str,
                 male_names: List[str], female_names: List[str]) -> str:
    """Generate a random name based on gender.
    Parameters:character_symbol (str): The symbol representing the character.
        symbol_description (str): A description of the character.
        gender (str): The gender of the character ('male', 'female', or 'any').
        male_names (list): List of male names.
        female_names (list): List of female names.
    Returns: str: The selected name or the character symbol if no name is available."""
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

class Plotter:
    """A class for generating plots based on predefined data and templates.
        Attributes:
            plotto (dict): The data used for generating plots.
            flip_genders (bool): Whether to flip the genders of the characters."""
    def __init__(self, plotto_data, flip_genders=False):
        """Initialize the Plotter class.
            Parameters:
            plotto_data (dict): Data for plot generation.
            flip_genders (bool): Whether to flip character genders."""
        self.plotto = plotto_data
        self.flip_genders = flip_genders

    def _picker(self, items: List, label: Optional[str] = None) -> Optional[str]:
        """Randomly pick an item from a list.
               Parameters:
                   items (list): The list to pick from.
                   label (str, optional): A label for debugging purposes.
               Returns:Any: A randomly selected item or None if the list is empty."""
        if not items:
            if label:
                print(f"No items to pick from for label: {label}")
            return None
        return random.choice(items)

    def generate(self):
        """Generate a plot based on the provided data.
            Returns:dict: A dictionary containing the generated plot details."""
        flip = self.flip_genders
        if flip is None:
            flip = random.choice([True, False])

        root_transform = self._get_gender_transform() if flip else {}
        A_Clause = random_clause(self.plotto['A_Clauses'])
        C_Clause = random_clause(self.plotto['C_Clauses'])
        B_Clause = random_clause(self.plotto['B_Clauses'])

        # subject = f"{C_Clause['group']} / {C_Clause['subgroup']}: {C_Clause['description']}"
        conflict = self.plotto['conflicts'][random_clause(B_Clause['nodes'])]
        cast = []
        plot = self._expand(conflict, root_transform, {"leadIns": 1, "carryOns": 1}, expand_id="root").replace('*', '')
        plot = self._apply_names(plot, cast)

        return {
            "group": B_Clause["group"],
            "subgroup": B_Clause["subgroup"],
            "description": B_Clause["description"],
            "cast": cast,
            "plot": f"{A_Clause}\n\n{plot}\n\n{C_Clause}".strip()
        }

    def _get_gender_transform(self):
        """Create a mapping to flip genders.
            Returns:dict: A dictionary mapping male identifiers to female and vice versa."""
        transform = {f"A-{i}": f"B-{i}" for i in range(10)}
        transform.update({f"B-{i}": f"A-{i}" for i in range(10)})
        return transform

    def _apply_names(self, text: str, cast: List[dict]) -> str:
        """Replace character symbols with names.
        Parameters:text (str): The text containing character symbols.
                   cast (list): A list to store character details.
        Returns:str: The text with character symbols replaced by names."""
        male_names = ["John", "David", "Michael", "Robert"]
        female_names = ["Mary", "Linda", "Barbara", "Elizabeth"]

        name_cache = {}
        rg = self._transform_to_regex(self.plotto['characters'])
        if rg:

            def replacer(match):
                symbol = match.group(0)
                if symbol in name_cache:
                    return name_cache[symbol]

                description = self.plotto['characters'].get(symbol, '')
                name = random_name(symbol, description, gender_map[symbol], male_names, female_names)
                name_cache[symbol] = name

                cast.append({"symbol": symbol, "name": name, "description": description})
                return name


            return re.sub(rg, replacer, text)

        return text

    def _transform_to_regex(self, mapping: dict) -> re.Pattern:
        """Create a regex pattern for matching character symbols.
             Parameters:mapping (dict): A dictionary of character symbols.
             Returns:re.Pattern: A compiled regex pattern."""
        keys = [str(key) for key in sorted(mapping.keys(), key=len, reverse=True)]
        if not keys:
            return re.compile(r'(?!x)x')  # Matches nothing
        pattern = r'\b(?:' + '|'.join(map(re.escape, keys)) + r')(?![a-z])'

        return re.compile(pattern)

    def _expand(self, item, transform, ctx, start=None, end=None, expand_id=""):
        """Expand an item recursively based on its structure.
        Parameters:item (any): The item to expand.
            transform (dict): A mapping for transformations.
            ctx (dict): Context for managing recursion.
            start (any, optional): Start range.
            end (any, optional): End range.
            expand_id (str, optional): Identifier for debugging.
        Returns:str: The expanded text."""
        ret = []
        expand_id = f"{expand_id}->{item}"  # Track unique expand ID
        if not item:
            return 'NULL'

        if ctx.get("leadIns", 0) > 0 and "leadIns" in item:
            ctx["leadIns"] -= 1
            ret.append(self._expand(item["leadIns"], None, ctx, expand_id=f"{expand_id}-leadIn"))

        carryon = None
        if ctx.get("carryOns", 0) > 0 and "carryOns" in item:
            ctx["carryOns"] -= 1
            carryon = self._expand(item["carryOns"], transform, ctx, expand_id=f"{expand_id}-carryOn")

        if isinstance(item, str):
            ret.append(self._expand(self.plotto["conflicts"].get(item, None), None, ctx, expand_id=f"{expand_id}-str"))
        elif isinstance(item, list):
            ret.append(self._expand(self._picker(item, "plot option"), None, ctx, expand_id=f"{expand_id}-list"))
        elif "conflictid" in item:
            if isinstance(item["description"], str):
                ret.append(item["description"])
            else:
                for subdesc in item["description"]:
                    if isinstance(subdesc, str):
                        ret.append(subdesc)
                    else:
                        ret.append(self._expand(subdesc, None, ctx, expand_id=f"{expand_id}-subdesc"))
        elif "v" in item:
            if item.get("start") or item.get("end"):
                ret.append(
                    self._expand(
                        self.plotto["conflicts"].get(item["v"], None),
                        item.get("tfm"),
                        ctx,
                        item.get("start"),
                        item.get("end"),
                        expand_id=f"{expand_id}-vstartend"
                    )
                )
            elif item.get("op") == "+":
                for sub in item["v"]:
                    ret.append(self._expand(sub, item.get("tfm"), ctx, expand_id=f"{expand_id}-vop"))
            else:
                ret.append(self._expand(item["v"], item.get("tfm"), ctx, expand_id=f"{expand_id}-v"))

        if carryon:
            ret.append(carryon)

        result = "\n\n".join(ret).strip()
        if transform:
            rg = self._transform_to_regex(transform)
            if rg:
                result = rg.sub(lambda m: transform.get(m.group(0), m.group(0)), result)
        return result


# Example usage
if __name__ == "__main__":
    with open("plotto_Clauses.json", "r") as f:
        plotto_data = json.load(f)

    generator = Plotter(plotto_data, flip_genders=False)
    plot = generator.generate()

    print("Generated Plot:")
    print(f"Group: {plot['group']}")
    print(f"Subgroup: {plot['subgroup']}")
    print(f"Description: {plot['description']}")
    print("Cast:")
    for character in plot['cast']:
        print(f"  - {character['name']} ({character['symbol']}): {character['description']}")
    print("\nPlot:")
    print(plot['plot'])
