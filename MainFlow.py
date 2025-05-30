import os

import claude_service
import helper_functions
from PlotGenie.PlotGenieBasic import PlotGenieBasic
from backend.Improvments import build_full_review_based_prompt
from backend.literary_evaluation_engine import generate_claude_evaluation_report


def mainFlow():
       ## create story skeleton based on plot genie and expand the story based on claude 3.7
        # pg = PlotGenieBasic()
        # prompt = pg.generate_prompt(word_count=1500, save=True)
        # story_response = claude_service.send_prompt_to_claude(prompt)
        # story_title = helper_functions.extract_title(story_response)
        # story_file_path = helper_functions.save_story_to_file(story_title, story_response)
        # ## literary evaluation based on claude 3.7
        #
        # result = generate_claude_evaluation_report(
        #     story_id=20,
        #     story_title=story_title,
        #     story_text=story_response
        # )
        # report_file_path = helper_functions.save_evaluation_report_to_file(result["story_id"], result["story_title"], result["raw_response"])
        #
        # ## improve story based on literary evaluation
        #
        # prompt = build_full_review_based_prompt(story_file_path, report_file_path)
        # improved_story_response = claude_service.send_prompt_to_claude(prompt)
        # improved_story_title = helper_functions.extract_title(improved_story_response) + "_improved"
        # helper_functions.save_story_to_file(improved_story_title, improved_story_response)
        #
        # print(improved_story_response)
        #
        # ## literary evaluation based on after improvement
        # result = generate_claude_evaluation_report(
        #     story_id=20,
        #     story_title=improved_story_title + "_improved",
        #     story_text=improved_story_response
        # )
        # improved_report_file_path = helper_functions.save_evaluation_report_to_file(result["story_id"], result["story_title"],
        #                                                                    result["raw_response"])

       # ===========================================================================================================================

        story_dir = 'PlottoStories'
        report_dir = 'PlottoReports'

        # קבלת רשימת הקבצים בתיקיות, ממוינת כדי לשמור על סדר תואם
        story_files = sorted(os.listdir(story_dir))
        report_files = sorted(os.listdir(report_dir))

        # לולאה על זוגות סדורים
        for i, (story_file, report_file) in enumerate(zip(story_files, report_files)):
            story_file_path = os.path.join(story_dir, story_file)
            report_file_path = os.path.join(report_dir, report_file)

            print("story_file_path = ", story_file_path)
            print("report_file_path = ", report_file_path)

            # בניית הפרומפט ושליחת הבקשה
            prompt = build_full_review_based_prompt(story_file_path, report_file_path)
            improved_story_response = claude_service.send_prompt_to_claude(prompt)

            # יצירת כותרת חדשה ושמירת הסיפור המשופר
            improved_story_title = helper_functions.extract_title(improved_story_response) + "_improved"
            helper_functions.save_story_to_file(improved_story_title, improved_story_response, "Improved_Stories")

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
                result["raw_response"], "Improved_Reports")


if __name__ == "__main__":
    mainFlow()
