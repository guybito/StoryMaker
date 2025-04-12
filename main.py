import importlib
import subprocess
import sys
from PlotGenieBasic import PlotGenieBasic

def install_if_missing(package_name, import_name=None):
    try:
        importlib.import_module(import_name or package_name)
        print(f"✔️  '{package_name}' is already installed.")
    except ImportError:
        print(f"📦 Installing '{package_name}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def parse_requirements_file(filename):
    requirements = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                # Remove version constraints for import check
                pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0]
                requirements.append((line, pkg_name.replace("-", "_")))
    return requirements

# Read and process requirements.txt
requirements = parse_requirements_file("requirements.txt")

# Check/install each requirement
for pip_name, import_name in requirements:
    install_if_missing(pip_name, import_name)

from PlotGenie import PlotGenie

# pg_basic = PlotGenieBasic()
pg = PlotGenie()

plot = pg.generate_plot(show_theme=True, save=True)
print(pg.describe_plot())
prompt = pg.generate_adaptive_prompt(1000)
print(prompt)