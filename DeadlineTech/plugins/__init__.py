import glob
from os.path import dirname, isfile, join


def __list_all_modules():
    work_dir = dirname(__file__)

    # Get modules in plugins/ folder
    mod_paths_main = glob.glob(join(work_dir, "*.py"))

    # Get modules inside subfolders (like tools/*.py)
    mod_paths_sub = glob.glob(join(work_dir, "*/*.py"), recursive=True)

    mod_paths = mod_paths_main + mod_paths_sub

    all_modules = [
        (((f.replace(work_dir, "")).replace("/", ".").replace("\\", "."))[:-3])
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
