from utils import load_names, load_gender_map, load_pronoun_map
from plotter import Plotter
import json
import os
#
#
def main():
    data_folder = "data"

    # Load data files
    with open(os.path.join(data_folder, "plotto_Clauses.json"), "r") as f:
        plotto_data = json.load(f)
    names_data = load_names(os.path.join(data_folder, "Actors_Names.json"))
    gender_map = load_gender_map(os.path.join(data_folder, "Gender_Map.json"))
    pronoun_map = load_pronoun_map(os.path.join(data_folder, "Pronoun_Map.json"))

    # Initialize the Plotter with the data
    generator = Plotter(
        plotto_data,gender_map,
        pronoun_map=pronoun_map,
        flip_genders=None,
        names_data=names_data,
    )

    # Generate the plot and build the graph dynamically
    plot = generator.generate(lead_ins=2, carry_ons=2)

    # Insert the C clause at the beginning and description at the end of the ordered sentences
    generator.ordered_sentences.append(plot["c clause"])
    generator.ordered_sentences.insert(0, plot["description"])

    # Print the generated plot details
    print("\nGenerated Plot:")
    print(f"A clause : {plot['a clause']}")
    print(f"Group: {plot['group']}")
    print(f"Subgroup: {plot['subgroup']}")
    print(f"Description = B clause : {plot['description']}")
    print("\nActors:")
    for character in generator.curr_name_mapping.items():
        print(f"  - {character[0]} : {character[1]}")

    # Prepare the ordered plot sentences
    ordered_plot = []
    for sentence_id in generator.ordered_sentences:
        for sentence in plot["plot"].split("\n"):
            if f"[{sentence_id}]" in sentence:
                ordered_plot.append(sentence.strip())
                break

    # Print the ordered plot
    print("\nPlot:")
    print(f"B clause : {plot['description']}")
    print("\n".join(ordered_plot))
    print(f"C clause : {plot['c clause']}")

    # Print the sentence IDs in order
    print("\nSentence Order (Ordered):")
    print(" -> ".join(generator.ordered_sentences))

    # Generate the graph representing the story-building process
    # generator.generate_graph(generator.ordered_sentences,plot)


if __name__ == "__main__":
    main()
