"""This module calls methods for seed script once called"""
from importlib import import_module
from pathlib import Path

# folder name containing the executable files for seed script
from app.utils.constants import DisplayMessage

exec_dir_name = "tasks"
base_path_format = str(Path(__name__))+".{}.{}"

"""
Update this with module names from /executables which contain execute()
method. These execute methods will contain a call to seed script related 
methods.
"""
seed_file_names = ["seed_db"]


def init_seed_script() -> None:
    """
    This method is used to run the seed script for the app after getting all
    the required functions
    :return: None
    """
    # collect all the file names and call it's execute method
    for file in seed_file_names:
        try:
            module = import_module(base_path_format.format(exec_dir_name,
                                                           file))
            execute = getattr(module, "execute")
            execute()
        except AttributeError:
            raise AttributeError(DisplayMessage.EXECUTE_MISSING.format(file))
        except ModuleNotFoundError:
            raise \
                ModuleNotFoundError(DisplayMessage.MODULE_MISSING.format(file))
        except Exception as err:
            raise err
