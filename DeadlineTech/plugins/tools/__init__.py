# DeadlineTech/plugins/tools/__init__.py

import glob
import os
from os.path import basename, dirname, isfile, join

# 📁 tools folder-ல் உள்ள அனைத்து .py files auto-import ஆகும்
MODULES_DIR = dirname(__file__)
ALL_MODULES = []

for file in glob.glob(join(MODULES_DIR, "*.py")):
    if isfile(file) and file.endswith(".py") and not file.endswith("__init__.py"):
        module_name = basename(file)[:-3]  # filename.py -> filename
        ALL_MODULES.append(module_name)
        __import__(f"{__name__}.{module_name}")
