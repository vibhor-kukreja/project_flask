import itertools
from functools import wraps
from typing import Dict, Callable

from app import failure


def validator(validator_fns: list) -> Callable:
    """
    A validator executor function, which executes the list of validator fns.
    :param validator_fns: List of validator functions. Every validator
    function is supposed to return a boolean.
    :return: A callable function
    """

    def _validator(f: callable) -> Callable:
        @wraps(f)
        def __validate(*args: tuple, **kwargs: dict) -> Dict:
            """
            This methods performs the validation
            process and return errors in any exists.
            :param args: tuple
            :param kwargs: dict
            :return:
            """
            errors = [validation_fn() for validation_fn in validator_fns]
            errors = list(itertools.chain.from_iterable(
                list(filter(lambda x: isinstance(x, list), errors))))
            if len(errors):
                return failure(message='Validation failed.', errors=errors)
            return f(*args, **kwargs)
        return __validate
    return _validator
