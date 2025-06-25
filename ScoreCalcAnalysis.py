import re
import os


def analyze_report_scores(file_path):
    total_overall_weighted_score = 0.0
    category_scores = {
        "Character": 0.0,
        "Conflict": 0.0,
        "Craft": 0.0,
        "Logic": 0.0
    }
    current_category = None

    category_pattern = re.compile(r"(?:##|\*\*)\s*([A-Za-z]+)\s*\(Category Weight = \d+\.\d+\)")
    weighted_score_pattern = re.compile(r".*?\**Weighted\s*Score\**:\s*(\d+\.\d+)", re.IGNORECASE)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "## Overall Weighted Score:" in line:
                    continue

                category_match = category_pattern.search(line)
                if category_match:
                    current_category = category_match.group(1).strip().capitalize()
                    continue

                score_match = weighted_score_pattern.search(line)
                if score_match:
                    score = float(score_match.group(1))
                    total_overall_weighted_score += score
                    if current_category and current_category in category_scores:
                        category_scores[current_category] += score

        return total_overall_weighted_score, category_scores, ""

    except FileNotFoundError:
        return 0.0, {}, f"Error: The file '{file_path}' was not found."
    except IOError as e:
        return 0.0, {}, f"Error reading file '{file_path}': {e}"


def update_overall_score_in_file(file_path, new_score):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            if line.strip().startswith("## Overall Weighted Score:"):
                updated_lines.append(f"## Overall Weighted Score: {new_score:.4f}\n")
            else:
                updated_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

    except Exception as e:
        print(f"❌ Failed to update file '{file_path}': {e}")


def run_analysis(report_directory='Results/Reports', output_file_name='Results/Reports_Score_Analysis.txt'):
    # Collect Reports
    try:
        files_in_directory = os.listdir(report_directory)
    except FileNotFoundError:
        print(f"Error: The directory '{report_directory}' was not found.")
        files_in_directory = []

    report_files = [f for f in files_in_directory if f.endswith('.txt')]

    # Write analysis to output file and fix report scores
    with open(output_file_name, 'w', encoding='utf-8') as outfile:
        if not report_files:
            outfile.write(f"No .txt files found in directory: {report_directory}.\n")
        else:
            report_files.sort()
            for file_name in report_files:
                full_file_path = os.path.join(report_directory, file_name)
                outfile.write(f"--- Processing File: {file_name} ---\n")

                overall_total, category_sums, error_message = analyze_report_scores(full_file_path)

                if error_message:
                    outfile.write(f"{error_message}\n")
                elif overall_total > 0 or any(category_sums.values()):
                    outfile.write(
                        f"Total Weighted Score for all questions (excluding overall line): {overall_total:.4f}\n\n")

                    outfile.write("Weighted Scores by Category:\n")
                    for category, total_score in category_sums.items():
                        outfile.write(f"  {category}: {total_score:.4f}\n")

                    sum_of_category_totals = sum(category_sums.values())
                    outfile.write(f"\nSum of all category totals: {sum_of_category_totals:.4f}\n")

                    update_overall_score_in_file(full_file_path, sum_of_category_totals)

                    if abs(overall_total - sum_of_category_totals) < 1e-9:
                        outfile.write(
                            "Verification: The sum of category totals matches the total weighted score for all questions.\n")
                    else:
                        outfile.write(
                            f"Verification: There is a discrepancy ({overall_total - sum_of_category_totals:.4f}) between the sum of category totals and the total weighted score for all questions.\n")
                else:
                    outfile.write(f"No valid 'Weighted Score' data found in '{file_name}' or an error occurred.\n")

                outfile.write("-" * 40 + "\n\n")

    print(f"✅ Analysis complete. Updated files and results written to '{output_file_name}'.")
