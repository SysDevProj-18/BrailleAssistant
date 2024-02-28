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
    " with ": " ⠾ ",
    " and ": " ⠯ ",
    " for ": " ⠿ ",
    "the ": "⠮ ",
    "ing": "⠬",
    "ble": "⠼", # removed in UEB
    " ": " ",

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

    "A": "⠠⠁",
    "B": "⠠⠃",
    "C": "⠠⠉",
    "D": "⠠⠙",
    "E": "⠠⠑",
    "F": "⠠⠋",
    "G": "⠠⠛",
    "H": "⠠⠓",
    "I": "⠠⠊",
    "J": "⠠⠚",
    "K": "⠠⠅",
    "L": "⠠⠇",
    "M": "⠠⠍",
    "N": "⠠⠝",
    "O": "⠠⠕",
    "P": "⠠⠏",
    "Q": "⠠⠟",
    "R": "⠠⠗",
    "S": "⠠⠎",
    "T": "⠠⠞",
    "U": "⠠⠥",
    "V": "⠠⠧",
    "W": "⠠⠺",
    "X": "⠠⠭",
    "Y": "⠠⠽",
    "Z": "⠠⠵",

    "0": "⠼⠚",
    "1": "⠼⠁",
    "2": "⠼⠃",
    "3": "⠼⠉",
    "4": "⠼⠙",
    "5": "⠼⠑",
    "6": "⠼⠋",
    "7": "⠼⠛",
    "8": "⠼⠓",
    "9": "⠼⠊",

    ".": ".",
    "!": "⠖",
    "?": "⠦",
    "'": "⠄",
    ";": "⠆",
    "<": "⠦",
    ">": "⠴",
}

def text_to_braille(text: str) -> str:
    regex = re.compile('|'.join(map(re.escape, BRAILLE_DICT)))
    return regex.sub(lambda match: BRAILLE_DICT[match.group(0)], text)

def text_to_braille1(text: str) -> str:
    global BRAILLE_DICT

    braille = ""
    while text:
        for i in BRAILLE_DICT.keys():
            if text[:len(i)] == i:
                text = text[len(i):]
                braille += BRAILLE_DICT[i]
                break
            elif i == '?':
                # handle no matching characters
                text = text[1:]
                braille += '?'
                break # <- probably redundant

    return braille

if __name__ == "__main__":
    print(text_to_braille(' '.join(sys.argv[1:])))
