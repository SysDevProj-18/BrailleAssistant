from data_structures import HalfCell


def dots_to_halfcells(dots: str) -> list[tuple[HalfCell, HalfCell]]:
    """
    Converts from liblouis dot sequences to a list of HalfCells.
    """
    return [_dots_to_halfcells(cell) for cell in "-".split(dots)]


def _dots_to_halfcells(dots: str) -> tuple[HalfCell, HalfCell]:
    if dots == "0":
        return HalfCell.NO_DOT, HalfCell.NO_DOT

    assert all(dot in "123456" for dot in dots)

    halftable = {
        "": HalfCell.NO_DOT,
        "1": HalfCell.TOP_DOT,
        "2": HalfCell.MIDDLE_DOT,
        "3": HalfCell.BOTTOM_DOT,
        "12": HalfCell.TOP_MIDDLE_DOT,
        "23": HalfCell.MIDDLE_BOTTOM_DOT,
        "123": HalfCell.ALL_DOTS,
    }

    left_half = "".join(i for i in dots if int(i) <= 3)
    right_half = "".join(str(int(i) % 3) for i in dots if int(i) > 3)

    return halftable[left_half], halftable[right_half]


_dt2br: dict[str, str] = {
    "0": "⠀",
    "1": "⠁",
    "2": "⠂",
    "12": "⠃",
    "3": "⠄",
    "13": "⠅",
    "23": "⠆",
    "123": "⠇",
    "4": "⠈",
    "14": "⠉",
    "24": "⠊",
    "124": "⠋",
    "34": "⠌",
    "134": "⠍",
    "234": "⠎",
    "1234": "⠏",
    "5": "⠐",
    "15": "⠑",
    "25": "⠒",
    "125": "⠓",
    "35": "⠔",
    "135": "⠕",
    "235": "⠖",
    "1235": "⠗",
    "45": "⠘",
    "145": "⠙",
    "245": "⠚",
    "1245": "⠛",
    "345": "⠜",
    "1345": "⠝",
    "2345": "⠞",
    "12345": "⠟",
    "6": "⠠",
    "16": "⠡",
    "26": "⠢",
    "126": "⠣",
    "36": "⠤",
    "136": "⠥",
    "236": "⠦",
    "1236": "⠧",
    "46": "⠨",
    "146": "⠩",
    "246": "⠪",
    "1246": "⠫",
    "346": "⠬",
    "1346": "⠭",
    "2346": "⠮",
    "12346": "⠯",
    "56": "⠰",
    "156": "⠱",
    "256": "⠲",
    "1256": "⠳",
    "356": "⠴",
    "1356": "⠵",
    "2356": "⠶",
    "12356": "⠷",
    "456": "⠸",
    "1456": "⠹",
    "2456": "⠺",
    "12456": "⠻",
    "3456": "⠼",
    "13456": "⠽",
    "23456": "⠾",
    "123456": "⠿",
}


def dots_to_braille(dots: str) -> str:
    """
    Translates liblouis dot sequences to braille text characters. Used for translation. Cells should be seperated by -
    """
    return "".join(_dt2br[c] for c in dots.split("-"))


_br2hc: dict[str, tuple[HalfCell, HalfCell]] = {
    "⠀": (HalfCell.NO_DOT, HalfCell.NO_DOT),
    "⠁": (HalfCell.TOP_DOT, HalfCell.NO_DOT),
    "⠂": (HalfCell.MIDDLE_DOT, HalfCell.NO_DOT),
    "⠃": (HalfCell.TOP_MIDDLE_DOT, HalfCell.NO_DOT),
    "⠄": (HalfCell.BOTTOM_DOT, HalfCell.NO_DOT),
    "⠅": (HalfCell.TOP_BOTTOM_DOT, HalfCell.NO_DOT),
    "⠆": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.NO_DOT),
    "⠇": (HalfCell.ALL_DOTS, HalfCell.NO_DOT),
    "⠈": (HalfCell.NO_DOT, HalfCell.TOP_DOT),
    "⠉": (HalfCell.TOP_DOT, HalfCell.TOP_DOT),
    "⠊": (HalfCell.MIDDLE_DOT, HalfCell.TOP_DOT),
    "⠋": (HalfCell.TOP_MIDDLE_DOT, HalfCell.TOP_DOT),
    "⠌": (HalfCell.BOTTOM_DOT, HalfCell.TOP_DOT),
    "⠍": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_DOT),
    "⠎": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.TOP_DOT),
    "⠏": (HalfCell.ALL_DOTS, HalfCell.TOP_DOT),
    "⠐": (HalfCell.NO_DOT, HalfCell.MIDDLE_DOT),
    "⠑": (HalfCell.TOP_DOT, HalfCell.MIDDLE_DOT),
    "⠒": (HalfCell.MIDDLE_DOT, HalfCell.MIDDLE_DOT),
    "⠓": (HalfCell.TOP_MIDDLE_DOT, HalfCell.MIDDLE_DOT),
    "⠔": (HalfCell.BOTTOM_DOT, HalfCell.MIDDLE_DOT),
    "⠕": (HalfCell.TOP_BOTTOM_DOT, HalfCell.MIDDLE_DOT),
    "⠖": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.MIDDLE_DOT),
    "⠗": (HalfCell.ALL_DOTS, HalfCell.MIDDLE_DOT),
    "⠘": (HalfCell.NO_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠙": (HalfCell.TOP_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠚": (HalfCell.MIDDLE_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠛": (HalfCell.TOP_MIDDLE_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠜": (HalfCell.BOTTOM_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠝": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠞": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.TOP_MIDDLE_DOT),
    "⠟": (HalfCell.ALL_DOTS, HalfCell.TOP_MIDDLE_DOT),
    "⠠": (HalfCell.NO_DOT, HalfCell.BOTTOM_DOT),
    "⠡": (HalfCell.TOP_DOT, HalfCell.BOTTOM_DOT),
    "⠢": (HalfCell.MIDDLE_DOT, HalfCell.BOTTOM_DOT),
    "⠣": (HalfCell.TOP_MIDDLE_DOT, HalfCell.BOTTOM_DOT),
    "⠤": (HalfCell.BOTTOM_DOT, HalfCell.BOTTOM_DOT),
    "⠥": (HalfCell.TOP_BOTTOM_DOT, HalfCell.BOTTOM_DOT),
    "⠦": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.BOTTOM_DOT),
    "⠧": (HalfCell.ALL_DOTS, HalfCell.BOTTOM_DOT),
    "⠨": (HalfCell.NO_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠩": (HalfCell.TOP_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠪": (HalfCell.MIDDLE_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠫": (HalfCell.TOP_MIDDLE_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠬": (HalfCell.BOTTOM_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠭": (HalfCell.TOP_BOTTOM_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠮": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.TOP_BOTTOM_DOT),
    "⠯": (HalfCell.ALL_DOTS, HalfCell.TOP_BOTTOM_DOT),
    "⠰": (HalfCell.NO_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠱": (HalfCell.TOP_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠲": (HalfCell.MIDDLE_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠳": (HalfCell.TOP_MIDDLE_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠴": (HalfCell.BOTTOM_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠵": (HalfCell.TOP_BOTTOM_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠶": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠷": (HalfCell.ALL_DOTS, HalfCell.MIDDLE_BOTTOM_DOT),
    "⠸": (HalfCell.NO_DOT, HalfCell.ALL_DOTS),
    "⠹": (HalfCell.TOP_DOT, HalfCell.ALL_DOTS),
    "⠺": (HalfCell.MIDDLE_DOT, HalfCell.ALL_DOTS),
    "⠻": (HalfCell.TOP_MIDDLE_DOT, HalfCell.ALL_DOTS),
    "⠼": (HalfCell.BOTTOM_DOT, HalfCell.ALL_DOTS),
    "⠽": (HalfCell.TOP_BOTTOM_DOT, HalfCell.ALL_DOTS),
    "⠾": (HalfCell.MIDDLE_BOTTOM_DOT, HalfCell.ALL_DOTS),
    "⠿": (HalfCell.ALL_DOTS, HalfCell.ALL_DOTS),
}


def braille_to_halfcells(braille: str) -> list[tuple[HalfCell, HalfCell]]:
    """
    Translates braille text characters to HalfCells. Used for final display.
    """
    assert is_braille(braille)
    return [_br2hc[c] for c in braille]


def is_braille(text: str) -> bool:
    """
    Returns true if text contains only braille representation characters. Returns false otherwise.
    """
    return all(c in _br2hc.keys() for c in text)
