import json
import os
import claude_service
import helper_functions
from PlotGenie.PlotGenieBasic import PlotGenieBasic
from AutomatedLiteraryCritique.Improvments import build_full_review_based_prompt
from AutomatedLiteraryCritique.literary_evaluation_engine import generate_claude_evaluation_report
from Plotto.helper_funcs import load_names, load_gender_map, load_pronoun_map
from Plotto.plotterrecursionbasedmainconflict import PlotterRecursionBasedMainConflict


def mainFlow(algo_name ):
    for i in range(0, 1):    ## create story skeleton based on plot genie and expand the story based on claude 3.7
        if algo_name == 'p':
            data_folder = "Plotto\data"
            # Load data files
            with open(os.path.join(data_folder, "plotto_Clauses.json"), "r", encoding="utf-8") as f:
                plotto_data = json.load(f)
            names_data = load_names(os.path.join(data_folder, "Actors_Names.json"))
            gender_map = load_gender_map(os.path.join(data_folder, "Gender_Map.json"))
            pronoun_map = load_pronoun_map(os.path.join(data_folder, "Pronoun_Map.json"))
            generatorBasedMainConflict = PlotterRecursionBasedMainConflict(
                plotto_data, gender_map,
                pronoun_map=pronoun_map,
                flip_genders=None,
                names_data=names_data,
            )
            plot = generatorBasedMainConflict.generate(lead_ins=2, carry_ons=2)
            prompt = generatorBasedMainConflict.generate_prompt(plot, 1500)
        else:
            pg = PlotGenieBasic()
            prompt = pg.generate_prompt(word_count=1500, save=True)
        story_response = claude_service.send_prompt_to_claude(prompt)
        print(story_response)
        story_title = helper_functions.extract_title(story_response)
        story_file_path = helper_functions.save_story_to_file(story_title, story_response)
            ## literary evaluation based on claude 3.7

        result = generate_claude_evaluation_report(
            story_id=i,
            story_title=story_title,
            story_text=story_response
        )
        report_file_path = helper_functions.save_evaluation_report_to_file(result["story_id"], result["story_title"], result["raw_response"])


    story_dir = 'PlottoStories'
    report_dir = 'PlottoReports'

    # קבלת רשימת הקבצים בתיקיות, ממוינת כדי לשמור על סדר תואם
    story_files = sorted(os.listdir(story_dir))
    report_files = sorted(os.listdir(report_dir))

    # לולאה על זוגות סדורים
    for i, (story_file, report_file) in enumerate(zip(story_files, report_files)):
        story_file_path = os.path.join(story_dir, story_file)
        report_file_path = os.path.join(report_dir, report_file)

        # בניית הפרומפט ושליחת הבקשה
        prompt = build_full_review_based_prompt(story_file_path, report_file_path)
        improved_story_response = claude_service.send_prompt_to_claude(prompt)

        # יצירת כותרת חדשה ושמירת הסיפור המשופר
        improved_story_title = helper_functions.extract_title(improved_story_response) + "_Plotto_improved"
        helper_functions.save_story_to_file(improved_story_title, improved_story_response)

        # הפקת דוח הערכה לסיפור המשופר
        result = generate_claude_evaluation_report(
            story_id=i,
            story_title=improved_story_title,
            story_text=improved_story_response
        )

        # שמירת הדוח החדש
        improved_report_file_path = helper_functions.save_evaluation_report_to_file(
            result["story_id"],
            result["story_title"],
            result["raw_response"]
        )
