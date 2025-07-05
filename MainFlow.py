import json
import os

import claude_service
import helper_functions
from HTML import convert_story_to_html
from PlotGenie.PlotGenieBasic import PlotGenieBasic
from Plotto.helper_funcs import load_names, load_gender_map, load_pronoun_map
from Plotto.plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict
from AutomatedLiteraryCritique.Improvments import build_full_review_based_prompt
from AutomatedLiteraryCritique.literary_evaluation_engine import generate_claude_evaluation_report
from ScoreCalcAnalysis import run_analysis


def mainFlow(algorithm_type, stories_amount=1, words_in_story_amount=2000, improve=True, create_html=True):
    data_folder = "Plotto\data"
    pg = PlotGenieBasic()
    for i in range(stories_amount):
        # ------------------------------------------- Story Creation - Plotto -------------------------------------------
        if algorithm_type == "Plotto":
            with open(os.path.join(data_folder, "plotto_Clauses.json"), "r", encoding="utf-8") as f:
                plotto_data = json.load(f)
            names_data = load_names(os.path.join(data_folder, "Actors_Names.json"))
            gender_map = load_gender_map(os.path.join(data_folder, "Gender_Map.json"))
            pronoun_map = load_pronoun_map(os.path.join(data_folder, "Pronoun_Map.json"))
            generator_based_main_conflict = PlotterRecursionBasedMainConflict(plotto_data, gender_map,
                                                                              pronoun_map=pronoun_map,
                                                                              flip_genders=None, names_data=names_data)
            plot = generator_based_main_conflict.generate(lead_ins=5, carry_ons=5)
            prompt = generator_based_main_conflict.generate_prompt(plot_string=plot, word_count=words_in_story_amount,
                                                                   save=True)
        # ---------------------------------------------------------------------------------------------------------------

        # ----------------------------------------- Story Creation - Plot Genie -----------------------------------------
        elif algorithm_type == "PlotGenie":
            # create story skeleton based on plot genie and expand the story based on claude 3.7
            prompt = pg.generate_prompt(word_count=words_in_story_amount, save=True)
        # ---------------------------------------------------------------------------------------------------------------

        # ----------------------------------------------- Story Creation ------------------------------------------------
        else:
            print("Invalid algorithm type")
            return

        story_response = claude_service.send_prompt_to_claude(prompt)
        story_title = helper_functions.extract_title(story_response)
        story_file_path = helper_functions.save_story_to_file(i + 1, algorithm_type, story_title, story_response)

        # -------------------------------------------- Story Report Creation --------------------------------------------

        # literary evaluation based on claude 3.7
        result = generate_claude_evaluation_report(
            story_id=i,
            story_title=story_title,
            story_text=story_response
        )

        report_file_path = helper_functions.save_evaluation_report_to_file(i + 1, algorithm_type, result["story_title"],
                                                                           result["raw_response"])
        # ---------------------------------------------------------------------------------------------------------------

        # ---------------------------------------------- Story Improvement ----------------------------------------------
        if improve:
            # improve story based on literary evaluation
            prompt = build_full_review_based_prompt(story_file_path, report_file_path)
            improved_story_response = claude_service.send_prompt_to_claude(prompt)
            improved_story_title = helper_functions.extract_title(improved_story_response) + "_improved"
            improved_story_file_path = helper_functions.save_story_to_file(i + 1, algorithm_type, improved_story_title,
                                                                           improved_story_response)

        # ---------------------------------------------------------------------------------------------------------------

        # -------------------------------------- Story Improvement Report Creation --------------------------------------

            # literary evaluation based on after improvement
            result = generate_claude_evaluation_report(
                story_id=i,
                story_title=improved_story_title + "_improved",
                story_text=improved_story_response
            )
            improved_report_file_path = helper_functions.save_evaluation_report_to_file(i + 1, algorithm_type,
                                                                                        result["story_title"],
                                                                                        result["raw_response"])
        # ---------------------------------------------------------------------------------------------------------------

        # ------------------------------------------------ Run Analysis -------------------------------------------------
        run_analysis()
        # ---------------------------------------------------------------------------------------------------------------

        # ---------------------------------------------- Create HTML Files ----------------------------------------------
        if create_html:
            convert_story_to_html(story_file_path, report_file_path, story_title + ".html")
            if improve:
                convert_story_to_html(improved_story_file_path, improved_report_file_path, improved_story_title + ".html")
        # ---------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # mainFlow_Plot_Genie(stories_amount=1, words_in_story_amount=2000, create_html=True)
    mainFlow("PlotGenie", stories_amount=20, words_in_story_amount=5000, improve=True, create_html=True)
    mainFlow("Plotto", stories_amount=20, words_in_story_amount=5000, improve=True, create_html=True)
    # mainFlow("Plotto", stories_amount=20, words_in_story_amount=5000, improve=False, create_html=True)
    # mainFlow("PlotGenie", stories_amount=20, words_in_story_amount=5000, improve=False, create_html=True)
