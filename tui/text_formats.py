import random

class ForegroundColours:
    """
    Enum shortcuts for ANSI foreground colour codes.
    """
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39

    @classmethod
    def random(cls):
        return random.randint(30, 37)


class BackgroundColours:
    """
    Enum shortcuts for ANSI background colour codes.
    """
    TRANSPARENT = -1
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    DEFAULT = 49

    @classmethod
    def random(cls):
        return random.randint(40, 47)


class TextFormats:
    """
    Enum shortcuts for ANSI text formatting codes.
    Only those that are commonly implemented are available.
    """
    DEFAULT = 0
    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4
    UNDERLINE_AND_BOLD = '1;4' # experimental
