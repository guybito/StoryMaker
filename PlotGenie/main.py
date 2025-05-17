# import importlib
# import subprocess
# import sys
from PlotGenieBasic import PlotGenieBasic
import re
import helper_functions
# # pg_basic = PlotGenieBasic()
# pg = PlotGenie()
#
# # plot = pg.generate_plot(save=True)
#

# prompt = pg.generate_adaptive_prompt(word_count=500, generate_plot=True, save=True)
# print(prompt)


# from PlotGenie import PlotGenie
#
#
# def run_cli():
#     print("🎬 Welcome to Plot Genie - Story Prompt Creator")
#
#     # 1. Random genre or manual?
#     random_choice = input("Choose genre randomly? (y/n): ").strip().lower()
#     if random_choice == 'y':
#         selected_genre = None
#         print("🎲 Random genre will be selected.")
#     else:
#         # Manual genre selection
#         genres = ['Romance', 'Adventure', 'Mystery', 'Comedy', 'Dramatic']
#         print("Choose a genre:")
#         for idx, g in enumerate(genres, 1):
#             print(f"{idx}. {g}")
#         genre_index = int(input("Enter number (1–5): ").strip()) - 1
#         selected_genre = genres[genre_index]
#         print(f"✅ Selected genre: {selected_genre}")
#
#     # 2. Word count
#     word_count = int(input("Enter desired word count (e.g., 1500, 5000, 10000): ").strip())
#
#     # 3. Developer-only: regenerate plot or reuse
#     # regenerate = input("Generate a new plot? (y/n): ").strip().lower() == "y"
#     # use_existing_plot = not regenerate
#
#     # 4. Developer-only: save output?
#     save_output = input("Save plot and prompt to file? (y/n): ").strip().lower() == "y"
#
#     # Run generation
#     genie = PlotGenie()
#     prompt = genie.generate_adaptive_prompt(
#         word_count,
#         generate_plot=True,
#         save=save_output,
#         genre=selected_genre
#     )
#
#     print("\n📜 Generated Prompt:\n" + "-" * 40)
#     print(prompt)

import claude_service

if __name__ == "__main__":
    # run_cli()

    pg = PlotGenieBasic()
    prompt = pg.generate_prompt(word_count=1500, save=True)
    response = claude_service.send_prompt_to_claude(prompt)
    story_title = helper_functions.extract_title(response)
    helper_functions.save_story_to_file(story_title, response)
    print(response)
