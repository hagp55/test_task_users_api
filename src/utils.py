import random
import string


def get_random_lower_string() -> str:
    """
    Generates a random lowercase string of a random length between 3 and 15 characters.

    Returns:
        str: A random lowercase string.
    """
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 15)))
