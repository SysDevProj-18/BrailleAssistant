from enum import IntEnum


class HalfCell(IntEnum):
    NO_DOT = 0
    TOP_DOT = 1
    MIDDLE_DOT = 2
    BOTTOM_DOT = 3
    TOP_MIDDLE_DOT = 4
    MIDDLE_BOTTOM_DOT = 5
    TOP_BOTTOM_DOT = 6
    ALL_DOTS = 7


BRAILLE_DICT: dict[str, tuple[HalfCell, HalfCell]] = {
    " ": (HalfCell.NO_DOT, HalfCell.NO_DOT),
    "a": (HalfCell.TOP_DOT, HalfCell.NO_DOT),
    "b": (HalfCell.TOP_MIDDLE_DOT, HalfCell.NO_DOT),
    "c": (HalfCell.TOP_DOT, HalfCell.TOP_DOT),
    "d": (HalfCell.TOP_DOT, HalfCell.TOP_MIDDLE_DOT),
    "e": (HalfCell.TOP_DOT, HalfCell.MIDDLE_DOT),
    "f": (HalfCell.TOP_MIDDLE_DOT, HalfCell.TOP_DOT),
    "g": (HalfCell.TOP_MIDDLE_DOT, HalfCell.TOP_MIDDLE_DOT),
    "h": (HalfCell.TOP_MIDDLE_DOT, HalfCell.MIDDLE_DOT),
    "i": (HalfCell.MIDDLE_DOT, HalfCell.TOP_DOT),
    "j": (HalfCell.MIDDLE_DOT, HalfCell.TOP_MIDDLE_DOT),
    "k": (HalfCell.TOP_BOTTOM_DOT, HalfCell.NO_DOT),
    "l": (HalfCell.ALL_DOTS, HalfCell.NO_DOT),
    "m": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_DOT),
    "n": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_MIDDLE_DOT),
    "o": (HalfCell.TOP_BOTTOM_DOT, HalfCell.MIDDLE_DOT),
    "p": (HalfCell.ALL_DOTS, HalfCell.TOP_DOT),
    "q": (HalfCell.ALL_DOTS, HalfCell.TOP_MIDDLE_DOT),
    "r": (HalfCell.ALL_DOTS, HalfCell.MIDDLE_DOT),
    "s": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.TOP_DOT),
    "t": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.TOP_MIDDLE_DOT),
    "u": (HalfCell.TOP_BOTTOM_DOT, HalfCell.BOTTOM_DOT),
    "v": (HalfCell.ALL_DOTS, HalfCell.BOTTOM_DOT),
    "w": (HalfCell.MIDDLE_DOT, HalfCell.ALL_DOTS),
    "x": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_BOTTOM_DOT),
    "y": (HalfCell.TOP_BOTTOM_DOT, HalfCell.ALL_DOTS),
    "z": (HalfCell.TOP_BOTTOM_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
}
