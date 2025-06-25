import unittest
import os
from PlotGenie import PlotGenie


class TestAdvancedPlotGenie(unittest.TestCase):

    def setUp(self):
        self.pg = PlotGenie(seed=123)

    def test_generate_plot_returns_valid_structure(self):
        """Test that the generated plot contains all expected keys."""
        plot = self.pg.generate_plot()
        required_keys = {"Locale", "Hero", "Beloved", "Problem", "Obstacle", "Complication", "Predicament", "Crisis", "Climax"}
        self.assertEqual(set(plot.keys()), required_keys)

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
