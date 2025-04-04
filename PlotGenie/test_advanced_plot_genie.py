import unittest
import os
from PlotGenie import PlotGenie, get_theme, filter_by_theme, THEMATIC_KEYWORDS


class TestAdvancedPlotGenie(unittest.TestCase):

    def setUp(self):
        self.pg = PlotGenie(seed=123)

    def test_generate_plot_returns_valid_structure(self):
        """Test that the generated plot contains all expected keys."""
        plot = self.pg.generate_plot()
        required_keys = {"Locale", "Hero", "Beloved", "Problem", "Obstacle", "Complication", "Predicament", "Crisis", "Climax"}
        self.assertEqual(set(plot.keys()), required_keys)

    def test_theme_identification_from_combined_text(self):
        """Test that get_theme correctly identifies a theme from combined problem and obstacle text."""
        theme = get_theme("He must recover a lost person", "who has been kidnapped")
        self.assertEqual(theme, "lost loved one")

    def test_theme_filter_effectiveness(self):
        """Test that filter_by_theme returns results relevant to the selected theme."""
        # pick a known theme and search for at least one match
        theme = "false accusation"
        category = self.pg.predicaments
        filtered = filter_by_theme(category, theme)
        self.assertTrue(any(any(kw in item.lower() for kw in THEMATIC_KEYWORDS[theme]) for item in filtered))

    def test_save_plot_with_theme_filename(self):
        """Test that saving a plot includes the theme in the filename when applicable. Also cleans up test file."""
        # Run and save with theme
        plot = self.pg.generate_plot(save=True)
        theme = get_theme(plot["Problem"], plot["Obstacle"])
        expected_fragment = theme.replace(" ", "_").lower() if theme else None
        found = any(expected_fragment in f for f in os.listdir("Plot Genie Plots")) if expected_fragment else True
        self.assertTrue(found)

        # Cleanup created test file
        if expected_fragment:
            for f in os.listdir("Plot Genie Plots"):
                if expected_fragment in f:
                    os.remove(os.path.join("Plot Genie Plots", f))

    def test_numbering_continues_properly(self):
        """Test that file numbering increases even when previous files have or don't have theme suffixes. Also cleans up test files."""
        dir_path = "Plot Genie Plots"
        os.makedirs(dir_path, exist_ok=True)

        # Clean existing plot files
        for f in os.listdir(dir_path):
            if f.startswith("Plot_") and f.endswith(".txt"):
                os.remove(os.path.join(dir_path, f))

        # Simulate existing files: Plot_1.txt
        with open(os.path.join(dir_path, "Plot_1.txt"), "w") as f:
            f.write("dummy")

        # Generate new plot
        self.pg.generate_plot(save=True)

        # Now expect: Plot_2.txt or Plot_2_<theme>.txt
        files = os.listdir(dir_path)
        self.assertTrue(any(f.startswith("Plot_2") for f in files))

        # Cleanup
        for f in files:
            if f.startswith("Plot_"):
                os.remove(os.path.join(dir_path, f))


if __name__ == '__main__':
    unittest.main()
