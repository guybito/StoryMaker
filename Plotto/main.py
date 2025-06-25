import claude_service
import helper_functions
from helper_funcs import load_names, load_gender_map, load_pronoun_map
from plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
import os
import json
import time
from claude_service import *


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
    with open(os.path.join(data_folder, "plotto_Clauses.json"), "r", encoding="utf-8") as f:
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
        write_to_file(dir_folder, folder_name, "\n".join(content))


        final_prompt_string = "\n".join(content)
        return final_prompt_string


    def generate_prompt(plot_string, word_count):
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
                                write the title of the story at the beginning of the story, in the next format: *the real title of the story*
            """

        return prompt

    # Call the functions
    base_folder = "Plotto Plots"
    # base_folder = "C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots"  # Replace with the actual base directory path
    main_conflict_folder = 'RecursionBasedMainConflict'
    lead_ins_folder = 'RecursionBasedLeadIns'
    plot = rec_based_main_conflict(base_folder, main_conflict_folder)
    prompt = generate_prompt(plot, 1500)
    response = claude_service.send_prompt_to_claude(prompt)
    story_title = helper_functions.extract_title(response)
    helper_functions.save_story_to_file(story_title, response)
    print(response)

if __name__ == "__main__":
    main()
