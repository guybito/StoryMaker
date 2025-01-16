
from helper_funcs import load_names, load_gender_map, load_pronoun_map
from plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
from PlotterRecursionBasedLeadIns import PlotterRecursionBasedLeadIns
import json
import api_backend
import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat, DocumentSchema, FunctionToolDefinition, ToolDefinition, ToolParameters




import time

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

        plot = generatorBasedMainConflict.generate(lead_ins=2, carry_ons=2)
        generatorBasedMainConflict.ordered_sentences.append(plot["c clause"])
        generatorBasedMainConflict.ordered_sentences.insert(0, plot["description"])

        content.append("\nGenerated Plot Based on Main Conflict Recursion:")
        content.append(f"A clause : {plot['a clause']}")
        content.append(f"Group: {plot['group']}")
        content.append(f"Subgroup: {plot['subgroup']}")
        content.append(f"Description = B clause : {plot['description']}")
        content.append("\nActors:")
        for character in generatorBasedMainConflict.curr_name_mapping.items():
            character_description = plotto_data["characters"].get(character[0])
            content.append(f"  - {character[0]} : {character[1]} - {character_description}")

        content.append(f'\nMain conflict: {plot["main conflict"]}')
        ordered_plot = []
        for sentence_id in generatorBasedMainConflict.ordered_sentences:
            for sentence in plot["plot"].split("\n"):
                if f"[{sentence_id}]" in sentence:
                    ordered_plot.append(sentence.strip())
                    break

        content.append("\n\nPlot:")
        content.append(f"B clause : {plot['description']}")
        content.extend(ordered_plot)
        content.append(f"\nC clause : {plot['c clause']}")

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
            character_description = plotto_data["characters"].get(character[0])
            content.append(f"  - {character[0]} : {character[1]} - {character_description}")

        content.append(f'\nMain conflict: {plot["main conflict"]}')
        ordered_plot = []
        for sentence_id in generatorBasedLeadIns.ordered_sentences:
            for sentence in plot["plot"].split("\n"):
                if f"[{sentence_id}]" in sentence:
                    ordered_plot.append(sentence.strip())
                    break

        content.append("\n\nPlot:")
        content.append(f"B clause : {plot['description']}")
        content.extend(ordered_plot)
        content.append(f"\nC clause : {plot['c clause']}")

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
    # main()
    # input_file_path = "C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots\\RecursionBasedMainConflict\\2.txt"
    # with open(input_file_path, "r") as file:
    #     file_content = file.read()
    # first_instruction = """
    # Im adding the skeleton of my story (a txt file) that detailed about a skeleton of a story (A theme about the main character of the story (under the title A clause), the theme of the story (under the the titles group and sub-group), the theme of the main conflict (under the title description),
    # the names and the description of the characters of the story (under the title actors), the description of the main conflict (under the title main conflict), the descriptions of each lead-in\carry-on of the main conflict
    # (under the title plot, it's already organized by order that means that the first description is the first lead-in and so on until the main conflict description and after will be the carry-ons by order until the c clause
    # and the description of the c clause (under the title c clause). this is some info about the meaning of each clause: The A Clause is the Protagonist Clause, The B Clause originates and carries on the action and the C Clause carries on and terminates the action.now after i explained about the input i gave you i want you please to give a title to the story based the info you have from the skeleton of the story (the txt file)
    # your response should be only the title without bolding or things like that! be the most creative you can!
    # """
    # second_instruction = """
    # Im adding the skeleton of my story (a txt file) that detailed about a skeleton of a story (A theme about the main character of the story (under the title A clause), the theme of the story (under the the titles group and sub-group), the theme of the main conflict (under the title description),
    # the names and the description of the characters of the story (under the title actors), the description of the main conflict (under the title main conflict), the descriptions of each lead-in\carry-on of the main conflict
    # (under the title plot, it's already organized by order that means that the first description is the first lead-in and so on until the main conflict description and after will be the carry-ons by order until the c clause
    # and the description of the c clause (under the title c clause). this is some info about the meaning of each clause: The A Clause is the Protagonist Clause, The B Clause originates and carries on the action and the C Clause carries on and terminates the action.now after i explained about the input i gave you i want you please to do the following (by order):1. give a title to the story based the info you have from the skeleton of the story (the txt file)
    # 2. i want you to write for me the opening of the story based on the info i gave you (using the info from the A clause and the actors), do it using maximum 60 words. 3. now i want you to expand the plot (using the info from the B clause, the main conflict and the plot), do it by expanding each paragraph in the plot to 75 words each. 4. now do the same you did for the opening of the story (in section 2) for the ending of the story (using the info from what you wrote in the previous section and the description of the c clause),
    # do it using maximum 60 words. most important make it looks like a story (without any numbering or titling paragraphs or things like that!, its should look like title and then paragraphs)
    # """
    # first_prompt = file_content + "  " + first_instruction
    # second_prompt = file_content + "\n\n" + second_instruction
    # api_backend.start_chat_gpt()
    # story_title = api_backend.make_gpt_request_and_copy(first_prompt.replace('\n', ' '))
    # print(f'the title is: {story_title}')
    # time.sleep(1)
    # story_content = api_backend.make_gpt_request_and_copy(second_prompt.replace('\n', ' '))
    # api_backend.stop_chat_gpt()
    #
    # output_file_path = f'C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots\\StoriesBasedMainConflict\\{story_title.strip()}.txt'
    #
    # # Write the content to the file
    # with open(output_file_path, "w") as file:
    #     file.write(story_content)
    # print(f"Output written to {output_file_path}")

    messages = [ChatMessage(content="Who was the first emperor of rome", role="user")]

    client = AI21Client()

    response = client.chat.completions.create(
        messages=messages,
        model="jamba-1.5-mini",
        stream=True
    )

    for chunk in response:
        print(chunk.choices[0].delta.content, end="")





