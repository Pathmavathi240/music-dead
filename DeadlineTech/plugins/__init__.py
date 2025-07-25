import glob
import os
from os.path import dirname, isfile, join

def __list_all_modules():
    work_dir = dirname(__file__)

    mod_paths_main = glob.glob(join(work_dir, "*.py"))
    mod_paths_sub = glob.glob(join(work_dir, "*/*.py"), recursive=True)

    mod_paths = mod_paths_main + mod_paths_sub

    all_modules = []
    for f in mod_paths:
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py"):
            rel_path = os.path.relpath(f, work_dir).replace("/", ".").replace("\\", ".")
            module_name = rel_path[:-3]  # .py நீக்கும்
            all_modules.append(module_name)

    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
