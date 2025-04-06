import importlib
import subprocess
import sys
from PlotGenieBasic import PlotGenieBasic

def install_if_missing(package_name, import_name=None):
    try:
        # Try to import the package (default to package_name if import_name not given)
        importlib.import_module(import_name or package_name)
        print(f"✔️  '{package_name}' is already installed.")
    except ImportError:
        print(f"📦 Installing '{package_name}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# List of packages to check/install
requirements = [
    ("huggingface-hub", "huggingface_hub"),
    ("sentence-transformers", "sentence_transformers")
]

# Run the installation check
for pip_name, import_name in requirements:
    install_if_missing(pip_name, import_name)

from PlotGenie import PlotGenie

# pg_basic = PlotGenieBasic()
pg = PlotGenie()

plot = pg.generate_plot(show_theme=True, save=True)
print(pg.describe_plot())
