from .. import Braille
HalfCell = Braille.HalfCell  # FIXME: figure out relative imports


def dots_to_halfcells(dots: str) -> list[tuple[HalfCell, HalfCell]]:
    """
    Converts from liblouis dot sequences to a list of HalfCells.
    """
    return [_dots_to_halfcells(cell) for cell in '-'.split(dots)]


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
        "123": HalfCell.ALL_DOTS
    }

    left_half = ''.join(i for i in dots if int(i) <= 3)
    right_half = ''.join(str(int(i) % 3) for i in dots if int(i) > 3)

    return halftable[left_half], halftable[right_half]


def dots_to_braille(dots: str) -> str:
    """
    TODO: Translates liblouis dot sequences to braille text characters. Used for translation.
    """
    raise NotImplementedError


def braille_to_halfcells(braille: str) -> list[tuple[HalfCell, HalfCell]]:
    """
    TODO: Translates braille text characters to HalfCells. Used for final display.
    """
    raise NotImplementedError

def is_braille(text: str) -> bool:
    """
    TODO: Returns true if text contains only braille representation characters. Returns false otherwise.
    """
    raise NotImplementedError