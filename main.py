# import importlib
# import subprocess
# import sys
# from PlotGenieBasic import PlotGenieBasic

# def install_if_missing(package_name, import_name=None):
#     try:
#         importlib.import_module(import_name or package_name)
#         print(f"✔️  '{package_name}' is already installed.")
#     except ImportError:
#         print(f"📦 Installing '{package_name}'...")
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
#
# def parse_requirements_file(filename):
#     requirements = []
#     with open(filename, "r") as file:
#         for line in file:
#             line = line.strip()
#             if line and not line.startswith("#"):
#                 # Remove version constraints for import check
#                 pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0]
#                 requirements.append((line, pkg_name.replace("-", "_")))
#     return requirements
#
# # Read and process requirements.txt
# requirements = parse_requirements_file("requirements.txt")
#
# # Check/install each requirement
# for pip_name, import_name in requirements:
#     install_if_missing(pip_name, import_name)

# from PlotGenie import PlotGenie
#
# # pg_basic = PlotGenieBasic()
# pg = PlotGenie()
#
# # plot = pg.generate_plot(save=True)
#
# prompt = pg.generate_adaptive_prompt(word_count=1000, generate_plot=True, save=True)
# print(prompt)

from PlotGenie import PlotGenie


def run_cli():
    print("🎬 Welcome to Plot Genie - Story Prompt Creator")
    print("Choose a genre:")
    genres = ['Romance', 'Adventure', 'Mystery', 'Comedy', 'Dramatic']
    for idx, g in enumerate(genres, 1):
        print(f"{idx}. {g}")

    genre_index = int(input("Enter number (1–5): ").strip()) - 1
    selected_genre = genres[genre_index]
    print(f"✅ Selected genre: {selected_genre}")

    word_count = int(input("Enter desired word count (e.g., 1500, 5000, 10000): ").strip())

    regenerate = input("Generate a new plot? (y/n): ").strip().lower() == "y"
    use_existing_plot = not regenerate

    save_output = input("Save plot and prompt to file? (y/n): ").strip().lower() == "y"

    genie = PlotGenie()

    prompt = genie.generate_adaptive_prompt(word_count, generate_plot=not use_existing_plot, save=save_output,
                                            genre=selected_genre)

    print("\n📜 Generated Prompt:\n" + "-" * 40)
    print(prompt)


if __name__ == "__main__":
    run_cli()
    # pg = PlotGenie()
    # pg.check_genre_filter_coverage(genre="Comedy", threshold=0.2)
