import re

import claude_service
import helper_functions
from helper_funcs import load_names, load_gender_map, load_pronoun_map
from plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
from PlotterRecursionBasedLeadIns import PlotterRecursionBasedLeadIns
# import api_backend
import os
# import requests
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


# prompt = """
# Role: you are story writing expert
# You are tasked with crafting an immersive and well-rounded story based on the provided plot
# framework. This story should be in modern English, engaging, vivid, and address key aspects of storytelling effectively. Follow these instructions closely to ensure a superior narrative.
#
#                      Plot Skeleton Format
#                     The plot framework will be provided in the following format:
#                     A Clause: Describes the initial state or identity of the protagonist or main subject of the story. It sets the stage for the story and establishes the baseline for what is about to change.
#                     Group: Indicates the overarching theme or genre of the story (e.g., Enterprise, Love, Adventure).
#                     Subgroup: Specifies the subgenre or nuanced theme within the group (e.g., Simulation, Redemption, Betrayal).
#                     B Clause: Outlines the central challenge, event, or action that sets the protagonist on their journey. This is the primary engine of the plot and often introduces the main conflict.
#                     Actors: Lists the key characters in the story, their names, and roles. These roles are indicated using placeholders (e.g., A, B, F-B, etc.) to show their relationship to the plot. The writer is expected to integrate these roles into the narrative with depth and distinction. (note: if the symbol X appears switch it in this way - an inanimate object, an object of mystery, an uncertain quantity, if Y\Z appear switch it with an exotic place that fits the plot).
# Plot Description: Provides a sequential outline of events that will shape the story, including pivotal moments, challenges, and character dynamics.
#                     C Clause: Concludes the narrative, indicating the resolution of the conflict and the ultimate fate of the characters.
#
#                     Story Requirements
#                     1. Character Development
#                     Clearly identify the protagonist and provide a compelling backstory that motivates their actions.
#                     Define the protagonist's goal or "want," ensuring they take an active role in achieving it.
#                     Include weaknesses, fears, or vulnerabilities that humanize the protagonist and make them relatable.
#                     Show a clear arc of change for the protagonist, where they grow, learn a lesson, or address their weaknesses by the end.
#                     Ensure supporting characters are distinct, colorful, and contribute meaningfully to the protagonist’s journey. Avoid stereotypes or unnecessary characters.
#                     Develop characters physically, mentally, and socially to create a multidimensional cast.
#                     2. Conflict
#                     Define a main conflict that is challenging and relatable, ensuring it sustains tension throughout the story.
#                     Relate the conflict to the human condition so it resonates with a broad audience.
#                     Incorporate external events and internal emotional struggles for both the protagonist and supporting characters.
#                     Introduce subplots with their own conflicts, which intertwine meaningfully with the main plot.
#                     Escalate the conflict effectively toward the climax, and ensure it is fully resolved by the end.
#                     3. Logic
#                     Avoid plot holes or inconsistencies. Ensure every detail aligns with established facts in the story.
#                     Clarify any potential ambiguities or unanswered questions to avoid reader confusion.
#                     Ensure all major elements are consistent with the internal logic of the story.
#                     4. Craft
#                     Use modern, vivid English with sophisticated word choice to create vivid imagery.
#                     Include rich descriptions of settings, characters, and actions to immerse readers in the story.
#                     Ensure the writing is clear, concise, and grammatically correct.
#                     5. Formatting Requirements
#                     Write the story in clear, distinct paragraphs for better readability.
#                     Provide a title that reflects the essence of the story.
#                     Ensure the story spans around 1500 words and delivers an engaging, complete narrative and being written in modern English
#                     6. Title
#                     write the title of the story at the beginning of the story, in the next format: *the real title of the story*
# """

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


        # content.append("\nSentence Order (Ordered):")
        # content.append(" -> ".join(generatorBasedMainConflict.ordered_sentences))
        # generatorBasedMainConflict.generate_graph(generatorBasedMainConflict.ordered_sentences, plot)
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
        write_to_file(dir_folder, folder_name, "\n".join(content))

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
    # rec_based_lead_ins(base_folder, lead_ins_folder)


if __name__ == "__main__":
    main()
    # story_title = ''
    # story_content = ''
    # api_key = "Dp3hMfNcVHebFcwEX1CX35xWFWgLrJY3"
    # input_file_path = "C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots\\RecursionBasedMainConflict\\10.txt"
    # with open(input_file_path, "r") as file:
    #     file_content = file.read()
    # second_instruction = """
    #                 You are tasked with crafting an immersive and well-rounded story based on the provided plot framework. This story should be engaging, vivid, and address key aspects of storytelling effectively. Follow these instructions closely to ensure a superior narrative.
    #                 Plot Skeleton Format
    #                 The plot framework will be provided in the following format:
    #                 A Clause: Describes the initial state or identity of the protagonist or main subject of the story. It sets the stage for the story and establishes the baseline for what is about to change.
    #                 Group: Indicates the overarching theme or genre of the story (e.g., Enterprise, Love, Adventure).
    #                 Subgroup: Specifies the subgenre or nuanced theme within the group (e.g., Simulation, Redemption, Betrayal).
    #                 B Clause: Outlines the central challenge, event, or action that sets the protagonist on their journey. This is the primary engine of the plot and often introduces the main conflict.
    #                 Actors: Lists the key characters in the story, their names, and roles. These roles are indicated using placeholders (e.g., A, B, F-B, etc.) to show their relationship to the plot. The writer is expected to integrate these roles into the narrative with depth and distinction. (note: if the symbol X appears switch it in this way - an inanimate object, an object of mystery, an uncertain quantity, if Y\Z appear switch it with an exotic place that fits the plot).
    #                 Plot Description: Provides a sequential outline of events that will shape the story, including pivotal moments, challenges, and character dynamics.
    #                 C Clause: Concludes the narrative, indicating the resolution of the conflict and the ultimate fate of the characters.
    #
    #                 Story Requirements
    #                 1. Character Development
    #                 Clearly identify the protagonist and provide a compelling backstory that motivates their actions.
    #                 Define the protagonist's goal or "want," ensuring they take an active role in achieving it.
    #                 Include weaknesses, fears, or vulnerabilities that humanize the protagonist and make them relatable.
    #                 Show a clear arc of change for the protagonist, where they grow, learn a lesson, or address their weaknesses by the end.
    #                 Ensure supporting characters are distinct, colorful, and contribute meaningfully to the protagonist’s journey. Avoid stereotypes or unnecessary characters.
    #                 Develop characters physically, mentally, and socially to create a multidimensional cast.
    #                 2. Conflict
    #                 Define a main conflict that is challenging and relatable, ensuring it sustains tension throughout the story.
    #                 Relate the conflict to the human condition so it resonates with a broad audience.
    #                 Incorporate external events and internal emotional struggles for both the protagonist and supporting characters.
    #                 Introduce subplots with their own conflicts, which intertwine meaningfully with the main plot.
    #                 Escalate the conflict effectively toward the climax, and ensure it is fully resolved by the end.
    #                 3. Craft
    #                 Use modern, vivid English with sophisticated word choice to create vivid imagery.
    #                 Include rich descriptions of settings, characters, and actions to immerse readers in the story.
    #                 Ensure the writing is clear, concise, and grammatically correct.
    #                 Use language to convey atmosphere, tension, and movement in an engaging way.
    #                 4. Dialogue
    #                 Craft dialogue that reflects each character's individuality and is appropriate for their background, time period, and personality.
    #                 Use dialogue to express subtext and layers of meaning, avoiding overly expository or platitudinal lines.
    #                 Ensure conversations flow naturally, contribute to character development, and advance the plot.
    #                 5. Subplot
    #                 Incorporate subplots that have a clear beginning, middle, and end, with challenges and reversals that add depth to the story.
    #                 Ensure subplots relate directly to the main plot and enrich the protagonist's journey.
    #                 Resolve subplots meaningfully, with a clear payoff.
    #                 6. Logic
    #                 Avoid plot holes or inconsistencies. Ensure every detail aligns with established facts in the story.
    #                 Clarify any potential ambiguities or unanswered questions to avoid reader confusion.
    #                 Ensure all major elements are consistent with the internal logic of the story.
    #                 7. Pacing
    #                 Balance action and dialogue for smooth narrative progression.
    #                 Maintain mystery and suspense throughout the story by introducing questions and revealing answers at the right time.
    #                 Ensure scenes flow logically and build causally ("this because this").
    #                 Include moments of anticipation, irony, or surprise that feel earned and align with the narrative.
    #                 8. Originality
    #                 Present an original premise that feels novel or refreshing within its genre.
    #                 Avoid over-reliance on clichés or recycled themes.
    #                 Introduce unique elements that make the story stand out, such as innovative character dynamics or unexpected twists.
    #                 9. Structure
    #                 Follow a clear beginning, middle, and end that forms a coherent whole.
    #                 Include structural beats (Pre‐Existing Life, Call to Action, Act One Decision, Midpoint, Climax, Resolution, etc.) at effective moments.
    #                 Ensure every scene drives the plot progression, character arc, or both.
    #                 Plant details early that pay off later in the narrative.
    #                 Formatting Requirements
    #                 Write the story in clear, distinct paragraphs for better readability.
    #                 Provide a title that reflects the essence of the story.
    #                 Ensure the story spans around 500 words and delivers an engaging, complete narrative and being written in modern English
    #                 """
    # second_prompt = file_content + "\n\n" + second_instruction
    # while True:
    #     user_input = input("Enter 'c' to create a story with chatGPT or 'j' to create a story with jamba: ").lower()
    #
    #     if user_input == 'c':
    #         first_instruction = """
    #             Im adding the skeleton of my story (a txt file) that detailed about a skeleton of a story (A theme about the main character of the story (under the title A clause), the theme of the story (under the the titles group and sub-group), the theme of the main conflict (under the title description),
    #             the names and the description of the characters of the story (under the title actors), the description of the main conflict (under the title main conflict), the descriptions of each lead-in\carry-on of the main conflict
    #             (under the title plot, it's already organized by order that means that the first description is the first lead-in and so on until the main conflict description and after will be the carry-ons by order until the c clause
    #             and the description of the c clause (under the title c clause). this is some info about the meaning of each clause: The A Clause is the Protagonist Clause, The B Clause originates and carries on the action and the C Clause carries on and terminates the action.now after i explained about the input i gave you i want you please to give a title to the story based the info you have from the skeleton of the story (the txt file)
    #             your response should be only the title without bolding or things like that! be the most creative you can!
    #             """
    #         # Assuming api_backend is defined elsewhere
    #         api_backend.start_chat_gpt()
    #         first_prompt = file_content + "  " + first_instruction
    #         story_title = api_backend.make_gpt_request_and_copy(first_prompt.replace('\n', ' '))
    #         print(f'the title is: {story_title}')
    #         time.sleep(1)
    #         story_content = api_backend.make_gpt_request_and_copy(second_prompt.replace('\n', ' '))
    #         api_backend.stop_chat_gpt()
    #         break  # Exit the loop after successful execution of 'c' part
    #
    #     elif user_input == 'j':
    #         url = 'https://api.ai21.com/studio/v1/chat/completions'
    #         headers = {
    #             'Authorization': f'Bearer {api_key}',
    #             'Content-Type': 'application/json'
    #         }
    #         payload = {
    #             "model": "jamba-1.5-large",
    #             "messages": [
    #                 {"role": "user", "content": second_prompt.replace('\n', ' ')}
    #             ],
    #             "maxTokens": 100,
    #             "temperature": 0.7
    #         }
    #
    #         response = requests.post(url, headers=headers, data=json.dumps(payload))
    #
    #         if response.status_code == 200:
    #             result = response.json()
    #             story_content = result['choices'][0]['message']['content']
    #             story_title = re.findall(r'\*\*(.*?)\*\*', story_content)
    #         else:
    #             print(f'Error: {response.status_code}')
    #             print(response.json())
    #         break  # Exit the loop after successful execution of 'j' part
    #
    #     else:
    #         print("Invalid input. Please enter 'c' or 'j'.")
    # output_file_path = f'C:\\SemesterG\\FinalProject\\Code\\GeneratedPlots\\StoriesBasedMainConflict\\{story_title[0].split("Title: ")[1]}.txt'
    # # Write the content to the file
    # with open(output_file_path, "w") as file:
    #     file.write(story_content)
    # print(f"Output written to {output_file_path}")
    #
    #
    #
    #
    #
    #
    #
