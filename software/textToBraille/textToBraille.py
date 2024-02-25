import logging

from Rules import *
from brailleFormats import *
from .. import Braille
HalfCell = Braille.HalfCell  # FIXME: figure out relative imports

# using Unified English Braille tables as they seem better maintained and more comprehensive.
DEFAULT_TABLE = "tables/en-ueb-g2.ctb"


def _translate_escapes(text: str) -> str:
    """
    TODO: Translates escape sequences in a string from the liblouis table format to the intended character.
    """
    raise NotImplementedError


class Table:
    """
    A class representing a (compiled) Braille translation table.

    Translation is implemented this way to avoid issues with garbage collection requiring recompilation of the tables
    for each translation. For efficiency reasons, this class implements little to no error checking(!). Please ensure
    all tables used work correctly with standard Liblouis before using them with this program.

    Usage:
    table = Table()
    table.translate("test")
    """

    def __init__(self, file=DEFAULT_TABLE):
        self.file = file  # A filename is used instead of a grade indicator to improve multi-language support.
        self.rules = {
            "pretrans": [],  # rules that translate text to text (replace)
            "pass1": [],  # first pass rules
            "pass2": [],  # second pass rules
            "pass3": [],  # third pass rules
            "pass4": []   # fourth pass rules
        }
        self.chargroups = {
            "space": [],
            "punctuation": [],
            "digit": [],
            "letter": [],
            "lowercase": [],
            "uppercase": [],
            "sign": [],
            "math": []
        }
        self._compile()

    def _compile(self):
        files = [self.file]
        while files:
            with open(files.pop()) as file:
                for line in file:
                    if line[0] == '#':  # skip comments
                        continue

                    tokens = ' '.split(_translate_escapes(line))
                    if tokens[0] == "include":
                        files.append("tables/" + tokens[1])
                        continue

                    self._parse_line(tokens)


    def _parse_line(self, tokens):
        match tokens[0]:
            case "noback":  # noback indicates following opcode is only for forward translation; just ignore here
                self._parse_line(tokens[1:])

            # character-definition opcodes
            case "space" | "punctuation" | "digit" | "letter" | "lowercase" | "uppercase" | "sign" | "math":
                self.chargroups[tokens[0]] += tokens[1]
                self.rules["pass1"] += CharacterRule(tokens[1], dots_to_braille(tokens[2]))
            case "base":  # hacky solution for characters based on another character
                self.chargroups[tokens[1]] += tokens[2]
                self.rules["pretrans"] += PretransRule(tokens[2], tokens[3])

            # not implemented opcodes; log warning and ignore
            case "display" | "litdigit" | "grouping":
                logging.warning(f"Unimplemented opcode {tokens[0]} used in table {self.file}")


    def translate(self, text: str) -> list[tuple[HalfCell]]:
        ...

