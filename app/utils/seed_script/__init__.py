"""This module calls methods for seed script once called"""
import inspect
from typing import List

from .seed_script_methods import SeedClass


def get_executables(class_name: object) -> List:
    """
    This method is supposed to take in a class and return all it's functions in
    a list
    :param class_name: A class which contains functions
    :return: List containing all executable functions of a class
    """
    return [method_name for
            (method_name, method_type) in inspect.getmembers(class_name)
            if inspect.isfunction(method_type)]


def initialize_seed_script() -> None:
    """
    This method is used to run the seed script for the app after getting all
    the required functions
    :return:
    """
    # get all the executable methods from classes
    executables = get_executables(SeedClass)
    try:
        for method in executables:
            # run each method
            eval(f"SeedClass.{method}()")
    except Exception as err:
        raise err
