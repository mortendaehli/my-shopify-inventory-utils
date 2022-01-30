from enum import Enum


class Language(str, Enum):
    """
    string corresponding to the url needed for correct translation. Do not change!
    """

    GERMAN = "de"
    ENGLISH = "en"
    DANISH = "da"
    NORWEGIAN = "no"
