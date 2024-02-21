#!/usr/bin/env/python3

"""
A quick and dirty one-way grade 2 text-to-braille converter for use in a worst-case scenario for the first demo.
Heavily unoptimized. Should be relatively simple to translate to Rust in the case where we want to iterate on this
solution instead of working with other libraries, but better algorithms probably exist.

Implemented according to Unified English Braille. Numerous edge cases will be produced incorrectly (such as ligatures
produced across compounds words like twOFold, shanGHai or gINGer) but as many have been filtered as is possible without
too much development time.
"""

import sys
import re

# please excuse starting a script with this wall instead of storing it separately; it should definitely be moved out for
# production but at this stage portability is key. lots of options for encoding this later!
BRAILLE_DICT = {
    " ing": "⠀⠊⠝⠛", # handle contractions that can't begin words
#   " ble": "⠀⠃⠇⠑", # removed in UEB

    " ": "⠀", # place space early for efficiency. note that the character in the value position is U+2800 dots-0

    "with": "⠾",
    "and": "⠯",
    "for": "⠿",
    "the": "⠮",
    "ing": "⠬",
#   "ble": "⠼", # removed in UEB

    "of": "⠷",
    "ch": "⠡",
    "gh": "⠣",
    "sh": "⠩",
    "th": "⠹",
    "wh": "⠱",
    "ed": "⠫",
    "er": "⠻",
    "ou": "⠳",
    "ow": "⠪",
    "ea": "⠂",
    "bb": "⠆",
    "cc": "⠒",
    "en": "⠢",
    "ff": "⠖",
    "gg": "⠶",
    "in": "⠔",

    "a": "⠁",
    "b": "⠃",
    "c": "⠉",
    "d": "⠙",
    "e": "⠑",
    "f": "⠋",
    "g": "⠛",
    "h": "⠓",
    "i": "⠊",
    "j": "⠚",
    "k": "⠅",
    "l": "⠇",
    "m": "⠍",
    "n": "⠝",
    "o": "⠕",
    "p": "⠏",
    "q": "⠟",
    "r": "⠗",
    "s": "⠎",
    "t": "⠞",
    "u": "⠥",
    "v": "⠧",
    "w": "⠺",
    "x": "⠭",
    "y": "⠽",
    "z": "⠵",

    "á": "⠈⠁",
    "é": "⠈⠑",
    "í": "⠈⠊",
    "ó": "⠈⠕",
    "ú": "⠈⠥",

    "à": "⠈⠁",
    "è": "⠈⠑",
    "ì": "⠈⠊",
    "ò": "⠈⠕",
    "ù": "⠈⠥",

    "â": "⠈⠁",
    "ê": "⠈⠑",
    "î": "⠈⠊",
    "ô": "⠈⠕",
    "û": "⠈⠥",

    "ä": "⠈⠁",
    "ë": "⠈⠑",
    "ï": "⠈⠊",
    "ö": "⠈⠕",
    "ü": "⠈⠥",

    "ā": "⠈⠁",
    "ē": "⠈⠑",
    "ī": "⠈⠊",
    "ū": "⠈⠕",
    "ō": "⠈⠥", # consider also implementing breve, haček, Ł, å, ogonek, đ, Ħ, ș, ø, and check umlaut/diarsesis cross-handling

    "ç": "⠈⠉",
    "ñ": "⠈⠝",

    ",": "⠂",
    ";": "⠆",
    ":": "⠒",
    "'": "⠄",
    "%": "⠨⠴",

    ".": "⠲⠠",
    "!": "⠖⠠", #WARNING: these three are followed by a capitalisation symbol as a stopgap solution
    "?": "⠦⠠",

    "#": "#" # fallback handling
}

def text_to_braille(text: str) -> str:
    regex = re.compile('|'.join(map(re.escape, BRAILLE_DICT)))
    return regex.sub(lambda match: BRAILLE_DICT[match.group(0)], text)

if __name__ == "__main__":
    print(text_to_braille(' '.join(sys.argv[1:])))
