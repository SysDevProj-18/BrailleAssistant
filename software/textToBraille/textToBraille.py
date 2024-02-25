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
    all tables used work correctly with standard Liblouis before using them with this program. Object instantiation
    involves an expensive compilation step, so try to avoid creating more instances than necessary.

    Usage:
    table = Table()
    table.translate("test")
    """

    def __init__(self, file=DEFAULT_TABLE):
        self.file = file  # A filename is used instead of a grade indicator to improve multi-language support.
        self.rules = {
            "pretrans": [],  # rules that translate text to text (replace)
            "urgent": [],  # always rules and the like that must precede translation
            "early": [],  # context dependent rules that need most of the string intact
            "pass1": [],  # first pass rules
            "pass2": [],  # second pass rules
            "pass3": [],  # third pass rules
            "pass4": [],  # fourth pass rules
            "charrules": []   # individual character translation rules; use at end
        }
        self.chargroups = {
            "space": [],
            "punctuation": [],
            "digit": [],
            "letter": [],
            "lowercase": [],
            "uppercase": [],
            "sign": [],
            "math": [],
            "_CAPSMODE": [],
            "_NUMMODE": [],
            "_NUMNOCONT": [],
            "_SEQDELIMITER": []
        }
        self.specialsymbols = {
            "decpoint": ("",""),
            "hyphen": ("", "")
        }
        self.indicators = {
            "undefined": "?"
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
            case "noback" | "nocross":  # opcode prefixes that can be ignored for our use case
                self._parse_line(tokens[1:])

            # character-definition opcodes
            case "space" | "punctuation" | "digit" | "letter" | "lowercase" | "uppercase" | "sign" | "math":
                self.chargroups[tokens[0]] += tokens[1]
                self.rules["charrules"] += CharacterRule(tokens[1], dots_to_braille(tokens[2]))
            case "base":  # hacky solution for characters based on another character
                self.chargroups[tokens[1]] += tokens[2]
                self.rules["pretrans"] += PretransRule(tokens[2], tokens[3])  # FIXME (?): indicators for base opcode
            case "attribute":
                if tokens[1] in self.chargroups.keys:
                    self.chargroups[tokens[1]] += tokens[2]
                else:
                    self.chargroups[tokens[1]] = [tokens[2]]  # handle creation of new character class

            # braille indicator opcodes
            case "modeletter":
                self.indicators[tokens[1] + "letter"] = dots_to_braille(tokens[2])
            case "capsletter":  # alias for 'modeletter uppercase'
                self.indicators["uppercaseletter"] = dots_to_braille(tokens[2])
            case "begmodeword":
                self.indicators[tokens[1] + "word"] = dots_to_braille(tokens[2])
            case "begcapsword":  # alias for 'begmodeword uppercase'
                self.indicators["uppercaseword"] = dots_to_braille(tokens[2])
            case "endmodeword":
                self.indicators[tokens[1] + "term"] = dots_to_braille(tokens[2])
            case "endcapsword":  # alias for 'endmodeword uppercase'
                self.indicators["uppercaseterm"] = dots_to_braille(tokens[2])
            case "begmode":
                self.indicators[tokens[1] + "beg"] = dots_to_braille(tokens[2])
            case "begcaps":  # alias for 'begmode uppercase'
                self.indicators["uppercasebeg"] = dots_to_braille(tokens[2])
            case "endmode":
                self.indicators[tokens[1] + "end"] = dots_to_braille(tokens[2])
            case "endcaps":  # alias for 'endmode caps'
                self.indicators["capsend"] = dots_to_braille(tokens[2])

            case "letsign": # set letter sign indicator
                self.indicators["letsign"] = dots_to_braille(tokens[1])
            case "nocontractsign": # only used for UEB (generally)
                self.indicators["nocontractsign"] = dots_to_braille(tokens[1])
            case "numsign":
                self.indicators["numsign"] = dots_to_braille(tokens[1])
            case "nonumsign":
                self.indicators["nonumsign"] = dots_to_braille(tokens[1])

            case "numericnocontchars":
                self.chargroups["_NUMNOCONT"] += tokens[1].split()
            case "numericmodechars":
                self.chargroups["_NUMMODE"] += tokens[1].split()

            # operators for UEB "Standing Alone" sequences
            case "seqdelimiter":
                ...
            case "seqbeforechars":
                ...
            case "seqafterchars":
                ...
            case "seqafterpattern":
                ...

            # special symbol opcodes
            case "decpoint":
                self.specialsymbols["decpoint"] = (tokens[1], dots_to_braille(tokens[2]))
            case "hyphen":
                self.specialsymbols["hyphen"] = (tokens[1], dots_to_braille(tokens[2]))

            # pretranslation opcodes
            case "correct":
                self.rules["pretrans"] += PretransRule(tokens[1], tokens[2])

            # translation opcodes
            case "always":
                self.rules["urgent"] += MapRule(tokens[1], dots_to_braille(tokens[2]))

            case "word":  # match if surrounded by whitespace / punctuation (only space and period for our use case)
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"(?=[\.\s])", dots_to_braille(tokens[2]))
            case "joinword":
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"[\.\s](?=\w)", dots_to_braille(tokens[2]))
            case "lowword":
                self.rules["early"] += MapRule(r"(?<=\s)" + tokens[1] + r"(?=\s)", dots_to_braille(tokens[2]))
            case "sufword":
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"(?=[\.\s\w])", dots_to_braille(tokens[2]))
            case "prfword":
                self.rules["early"] += MapRule(r"(?<=[\.\s\w])" + tokens[1] + r"(?=[\.\s])", dots_to_braille(tokens[2]))
            case "begword":
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"(?=\w)", dots_to_braille(tokens[2]))
            case "begmidword":
                self.rules["early"] += MapRule(r"(?<=[\.\s\w])" + tokens[1] + r"(?=\w)", dots_to_braille(tokens[2]))
            case "midword":
                self.rules["early"] += MapRule(r"(?<=\w)" + tokens[1] + r"(?=\w)", dots_to_braille(tokens[2]))
            case "midendword":
                self.rules["early"] += MapRule(r"(?<=\w)" + tokens[1] + r"(?=[\.\s\w])", dots_to_braille(tokens[2]))
            case "endword":
                self.rules["early"] += MapRule(r"(?<=\w)" + tokens[1] + r"(?=[\s\.])", dots_to_braille(tokens[2]))
            case "partword":
                self.rules["early"] += MapRule(r"((?<=\w)" + tokens[1] + "|" + tokens[1] + r"(?=\w))",
                                               dots_to_braille(tokens[2]))
            case "prepunc":
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"(?=[\.]*\w)", dots_to_braille(tokens[2]))
            case "postpunc":
                self.rules["early"] += MapRule(r"(?<=\w[\.]*)" + tokens[1] + r"(?=[\.\s])", dots_to_braille(tokens[2]))
            case "begnum":
                self.rules["early"] += MapRule(r"(?<=[\.\s])" + tokens[1] + r"(?=\d)", dots_to_braille(tokens[2]))
            case "midnum":
                self.rules["early"] += MapRule(r"(?<=\d)" + tokens[1] + r"(?=\d)", dots_to_braille(tokens[2]))
            case "endnum":
                self.rules["early"] += MapRule(r"(?<=\d)" + tokens[1] + r"(?=[\.\s])", dots_to_braille(tokens[2]))



            # context and multipass opcodes
            case "context":
                self.rules["pass1"] += LouisRule(tokens[1], tokens[2])
            case "pass2" | "pass3" | "pass4":
                self.rules[tokens[0]] += LouisRule(tokens[1], tokens[2])

            # match opcode
            case "match":
                self.rules["pass1"] += MatchRule((tokens[1], tokens[2], tokens[3]), tokens[4])

            # miscellaneous opcodes
            case "undefined":  # set character to be used for untranslatable text
                self.indicators["undefined"] = tokens[1]  # don't translate to braille (obviously)
            case "capsmodechars":  # add characters that will not automatically terminate uppercase mode
                self.chargroups["_CAPSMODE"] += tokens[1].split()

            # not implemented opcodes; log warning and ignore. most of these are for back translation purposes,
            # for braille applications not relevant to our simple sentence format, or just deprecated.
            case "display" | "litdigit" | "grouping" | "largesign" | "comprl" | "comp6" | "nocont" | "multind" | \
                 "swapcd" | "swapdd" | "swapcc" | "noletsign" | "noletsignbefore" | "noletsignafter" | \
                 "midendnumericmodechars" | "emphclass" | "begemph" | "endemph" | "noemphchars" | "emphletter" | \
                 "begemphword" | "endemphword" | "emphmodechars" | "begemphphrase" | "endemphphrase" | \
                 "lenemphphrase" | "begcomp" | "endcomp" | "capsnocont" | "replace" | "repeated" | "repword" | \
                 "rependword" | "syllable" | "contraction" | "exactdots" | "joinnum" | "after" | "before":
                logging.warning(f"Unimplemented opcode {tokens[0]} used in table {self.file}")

    def translate(self, text: str) -> list[tuple[HalfCell, HalfCell]]:
        # pretranslation step
        if self.rules["pretrans"]:
            for rule in self.rules["pretrans"]:
                text = rule(text, self.chargroups)

        # slight deviation from liblouis translation; handle priority rules before any passes
        if self.rules["priority"]:
            for rule in self.rules["priority"]:
                text = rule(text, self.chargroups)

        # first pass
        if self.rules["pass1"]:
            for rule in self.rules["pass1"]:
                text = rule(text, self.chargroups)

        # second pass
        if self.rules["pass2"]:
            for rule in self.rules["pass2"]:
                text = rule(text, self.chargroups)

        # third pass
        if self.rules["pass3"]:
            for rule in self.rules["pass3"]:
                text = rule(text, self.chargroups)

        # fourth pass
        if self.rules["pass4"]:
            for rule in self.rules["pass4"]:
                text = rule(text, self.chargroups)

        # clean up any missed characters using undefined character from tables
        text = ''.join(c if is_braille(c) else self.indicators["undefined"] for c in text)

        # translate to HalfCells and return
        return braille_to_halfcells(text)
