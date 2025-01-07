from utils import load_names, load_gender_map, load_pronoun_map
from plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
from PlotterRecursionBasedLeadIns import PlotterRecursionBasedLeadIns
import json
import os


def write_to_file(base_output_folder, folder_name, content):
    """Helper function to write content to a dynamically named file in a specific folder."""
    # Ensure the sub-folder exists
    function_folder = os.path.join(base_output_folder, folder_name)
    if not os.path.exists(function_folder):
        os.makedirs(function_folder)

    # Determine the next file name
    file_count = len(
        [name for name in os.listdir(function_folder) if os.path.isfile(os.path.join(function_folder, name))])
    file_path = os.path.join(function_folder, f"{file_count + 1}.txt")

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)
    print(f"Output written to {file_path}")


def main():
    data_folder = "data"
    # Load data files
    with open(os.path.join(data_folder, "plotto_Clauses.json"), "r") as f:
        plotto_data = json.load(f)
    names_data = load_names(os.path.join(data_folder, "Actors_Names.json"))
    gender_map = load_gender_map(os.path.join(data_folder, "Gender_Map.json"))
    pronoun_map = load_pronoun_map(os.path.join(data_folder, "Pronoun_Map.json"))

    def rec_based_main_conflict(dir_folder, folder_name):
        """Generate and save the output for main conflict recursion."""
        content = []
        generatorBasedMainConflict = PlotterRecursionBasedMainConflict(
            plotto_data, gender_map,
            pronoun_map=pronoun_map,
            flip_genders=None,
            names_data=names_data,
        )

        plot = generatorBasedMainConflict.generate(lead_ins=3, carry_ons=3)
        generatorBasedMainConflict.ordered_sentences.append(plot["c clause"])
        generatorBasedMainConflict.ordered_sentences.insert(0, plot["description"])

        content.append("\nGenerated Plot Based on Main Conflict Recursion:")
        content.append(f"A clause : {plot['a clause']}")
        content.append(f"Group: {plot['group']}")
        content.append(f"Subgroup: {plot['subgroup']}")
        content.append(f"Description = B clause : {plot['description']}")
        content.append("\nActors:")
        for character in generatorBasedMainConflict.curr_name_mapping.items():
            content.append(f"  - {character[0]} : {character[1]}")

        ordered_plot = []
        for sentence_id in generatorBasedMainConflict.ordered_sentences:
            for sentence in plot["plot"].split("\n"):
                if f"[{sentence_id}]" in sentence:
                    ordered_plot.append(sentence.strip())
                    break

        content.append("\nPlot:")
        content.append(f"B clause : {plot['description']}")
        content.extend(ordered_plot)
        content.append(f"C clause : {plot['c clause']}")

        content.append("\nSentence Order (Ordered):")
        content.append(" -> ".join(generatorBasedMainConflict.ordered_sentences))

        # generatorBasedMainConflict.generate_graph(generatorBasedMainConflict.ordered_sentences, plot)
        # print(content)
        write_to_file(dir_folder, folder_name, "\n".join(content))

    def rec_based_lead_ins(dir_folder, folder_name):
        """Generate and save the output for lead-ins recursion."""
        content = []
        generatorBasedLeadIns = PlotterRecursionBasedLeadIns(
            plotto_data, gender_map,
            pronoun_map=pronoun_map,
            flip_genders=None,
            names_data=names_data,
        )

        plot = generatorBasedLeadIns.generate(lead_ins=2, carry_ons=2)
        generatorBasedLeadIns.ordered_sentences.append(plot["c clause"])
        generatorBasedLeadIns.ordered_sentences.insert(0, plot["description"])

        content.append("\nGenerated Plot Based On Lead Ins Recursion:")
        content.append(f"A clause : {plot['a clause']}")
        content.append(f"Group: {plot['group']}")
        content.append(f"Subgroup: {plot['subgroup']}")
        content.append(f"Description = B clause : {plot['description']}")
        content.append("\nActors:")
        for character in generatorBasedLeadIns.curr_name_mapping.items():
            content.append(f"  - {character[0]} : {character[1]}")

        ordered_plot = []
        for sentence_id in generatorBasedLeadIns.ordered_sentences:
            for sentence in plot["plot"].split("\n"):
                if f"[{sentence_id}]" in sentence:
                    ordered_plot.append(sentence.strip())
                    break

        content.append("\nPlot:")
        content.append(f"B clause : {plot['description']}")
        content.extend(ordered_plot)
        content.append(f"C clause : {plot['c clause']}")

        content.append("\nSentence Order (Ordered):")
        content.append(" -> ".join(generatorBasedLeadIns.ordered_sentences))

        # generatorBasedLeadIns.generate_graph(generatorBasedLeadIns.ordered_sentences, plot)
        # print(content)
        write_to_file(dir_folder, folder_name, "\n".join(content))

    # Call the functions
    base_folder = "C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots"  # Replace with the actual base directory path
    main_conflict_folder = 'RecursionBasedMainConflict'
    lead_ins_folder = 'RecursionBasedLeadIns'
    rec_based_main_conflict(base_folder, main_conflict_folder)
    # rec_based_lead_ins(base_folder, lead_ins_folder)


if __name__ == "__main__":
    main()

# from utils import load_names, load_gender_map, load_pronoun_map
# from plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
# from PlotterRecursionBasedLeadIns import PlotterRecursionBasedLeadIns
# import json
# import os
#
#
# def main():
#     data_folder = "data"
#     # Load data files
#     with open(os.path.join(data_folder, "plotto_Clauses.json"), "r") as f:
#         plotto_data = json.load(f)
#     names_data = load_names(os.path.join(data_folder, "Actors_Names.json"))
#     gender_map = load_gender_map(os.path.join(data_folder, "Gender_Map.json"))
#     pronoun_map = load_pronoun_map(os.path.join(data_folder, "Pronoun_Map.json"))
#
#     def rec_based_main_conflict():
#         # Initialize the Plotter with the data
#         generator_based_main_conflict = PlotterRecursionBasedMainConflict(
#             plotto_data,gender_map,
#             pronoun_map=pronoun_map,
#             flip_genders=None,
#             names_data=names_data,
#         )
#
#         # Generate the plot and build the graph dynamically
#         plot = generator_based_main_conflict.generate(lead_ins=2, carry_ons=2)
#
#         # Insert the C clause at the beginning and description at the end of the ordered sentences
#         generator_based_main_conflict.ordered_sentences.append(plot["c clause"])
#         generator_based_main_conflict.ordered_sentences.insert(0, plot["description"])
#
#         # Print the generated plot details
#         print("\nGenerated Plot Based on Main Conflict Recursion:")
#         print(f"A clause : {plot['a clause']}")
#         print(f"Group: {plot['group']}")
#         print(f"Subgroup: {plot['subgroup']}")
#         print(f"Description = B clause : {plot['description']}")
#         print("\nActors:")
#         for character in generator_based_main_conflict.curr_name_mapping.items():
#             print(f"  - {character[0]} : {character[1]}")
#
#         # Prepare the ordered plot sentences
#         ordered_plot = []
#         for sentence_id in generator_based_main_conflict.ordered_sentences:
#             for sentence in plot["plot"].split("\n"):
#                 if f"[{sentence_id}]" in sentence:
#                     ordered_plot.append(sentence.strip())
#                     break
#
#         # Print the ordered plot
#         print("\nPlot:")
#         print(f"B clause : {plot['description']}")
#         print("\n".join(ordered_plot))
#         print(f"C clause : {plot['c clause']}")
#
#         # Print the sentence IDs in order
#         print("\nSentence Order (Ordered):")
#         print(" -> ".join(generator_based_main_conflict.ordered_sentences))
#
#         # Generate the graph representing the story-building process
#         # generator_based_main_conflict.generate_graph(generator_based_main_conflict.ordered_sentences,plot)
#
#     def rec_based_lead_ins():
#         # Initialize the Plotter with the data
#         generator_based_lead_ins = PlotterRecursionBasedLeadIns(
#             plotto_data, gender_map,
#             pronoun_map=pronoun_map,
#             flip_genders=None,
#             names_data=names_data,
#         )
#
#         # Generate the plot and build the graph dynamically
#         plot = generator_based_lead_ins.generate(lead_ins=2, carry_ons=2)
#
#         # Insert the C clause at the beginning and description at the end of the ordered sentences
#         generator_based_lead_ins.ordered_sentences.append(plot["c clause"])
#         generator_based_lead_ins.ordered_sentences.insert(0, plot["description"])
#
#         # Print the generated plot details
#         print("\nGenerated Plot Based On Lead Ins Recursion:")
#         print(f"A clause : {plot['a clause']}")
#         print(f"Group: {plot['group']}")
#         print(f"Subgroup: {plot['subgroup']}")
#         print(f"Description = B clause : {plot['description']}")
#         print("\nActors:")
#         for character in generator_based_lead_ins.curr_name_mapping.items():
#             print(f"  - {character[0]} : {character[1]}")
#
#         # Prepare the ordered plot sentences
#         ordered_plot = []
#         for sentence_id in generator_based_lead_ins.ordered_sentences:
#             for sentence in plot["plot"].split("\n"):
#                 if f"[{sentence_id}]" in sentence:
#                     ordered_plot.append(sentence.strip())
#                     break
#
#         # Print the ordered plot
#         print("\nPlot:")
#         print(f"B clause : {plot['description']}")
#         print("\n".join(ordered_plot))
#         print(f"C clause : {plot['c clause']}")
#
#         # Print the sentence IDs in order
#         print("\nSentence Order (Ordered):")
#         print(" -> ".join(generator_based_lead_ins.ordered_sentences))
#
#         # Generate the graph representing the story-building process
#         generator_based_lead_ins.generate_graph(generator_based_lead_ins.ordered_sentences, plot)
#
#     rec_based_main_conflict()
#     rec_based_lead_ins()
#
#
# if __name__ == "__main__":
#     main()
