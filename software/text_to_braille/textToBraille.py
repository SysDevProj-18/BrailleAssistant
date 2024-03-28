import logging

from .Rules import *
from .brailleFormats import *
from data_structures import HalfCell


# using Unified English Braille tables as they seem better maintained and more comprehensive.
DEFAULT_TABLE_G1 = "tables/en-ueb-g1.ctb"
DEFAULT_TABLE_G2 = "tables/en-ueb-g2.ctb"


class BrailleTranslator:
    """
    Simple wrapper class to allow hotswapping between contracted and uncontracted braille.
    """

    def __init__(self):
        self.g1 = Table(DEFAULT_TABLE_G1)
        self.g2 = Table(DEFAULT_TABLE_G2)

    def translate(self, text: str, contracted: bool) -> list[tuple[HalfCell, HalfCell]]:
        return self.g2.translate(text) if contracted else self.g1.translate(text)


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

    def __init__(self, file):
        self.file = file  # A filename is used instead of a grade indicator to improve multi-language support.
        self.rules = {
            "pretrans": [],  # rules that translate text to text (replace)
            "urgent": [],  # always rules and the like that must precede translation
            "early": [],  # context dependent rules that need most of the string intact
            "pass1": [],  # first pass rules
            "pass2": [],  # second pass rules
            "pass3": [],  # third pass rules
            "pass4": [],  # fourth pass rules
            "charrules": [
                CharacterRule(" ", "⠀")
            ],  # individual character translation rules; used at end
        }  # NB: space characters handled manually due to the need to strip whitespace
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
            "_": [],  # special group for unimplemented groups; will always be empty
        }
        self.specialsymbols = {"decpoint": ("", ""), "hyphen": ("", "")}
        self.indicators = {"undefined": "⠿"}
        self.variables = [0] * 50
        self._compile()

    def _compile(self):
        files = [self.file]
        while files:
            with open(files.pop()) as file:
                for line in file:
                    if line[0] == "#":  # skip comments
                        continue

                    tokens = translate_escapes(line).rstrip().split()

                    if not tokens:  # handle blank lines
                        continue
                    elif tokens[0] == "include":
                        files.append("tables/" + tokens[1])
                        continue

                    self._parse_line(tokens)

    def _parse_line(self, tokens):
        match tokens[0]:
            case (
                "noback"
                | "nocross"
            ):  # opcode prefixes that can be ignored for our use case
                self._parse_line(tokens[1:])

            # character-definition opcodes
            case (
                "space"
                | "punctuation"
                | "digit"
                | "letter"
                | "lowercase"
                | "uppercase"
                | "sign"
                | "math"
            ):
                self.chargroups[tokens[0]].append(tokens[1])
                self.rules["charrules"].append(
                    CharacterRule(tokens[1], dots_to_braille(tokens[2]))
                )
            case "base":  # hacky solution for characters based on another character
                self.chargroups[tokens[1]].append(tokens[2])
                self.rules["pretrans"].append(
                    MapRule(tokens[2], tokens[3])
                )  # FIXME (?): indicators for base opcode
                pass
            case "attribute":
                if tokens[1] in self.chargroups.keys():
                    self.chargroups[tokens[1]].append(tokens[2])
                else:
                    self.chargroups[tokens[1]] = [
                        tokens[2]
                    ]  # handle creation of new character class

            # braille indicator opcodes
            case "modeletter":
                self.indicators[tokens[1] + "letter"] = dots_to_braille(tokens[2])
            case "capsletter":  # alias for 'modeletter uppercase'
                self.indicators["uppercaseletter"] = dots_to_braille(tokens[1])
            case "begmodeword":
                self.indicators[tokens[1] + "word"] = dots_to_braille(tokens[2])
            case "begcapsword":  # alias for 'begmodeword uppercase'
                self.indicators["uppercaseword"] = dots_to_braille(tokens[1])
            case "endmodeword":
                self.indicators[tokens[1] + "term"] = dots_to_braille(tokens[2])
            case "endcapsword":  # alias for 'endmodeword uppercase'
                self.indicators["uppercaseterm"] = dots_to_braille(tokens[1])
            case "begmode":
                self.indicators[tokens[1] + "beg"] = dots_to_braille(tokens[2])
            case "begcaps":  # alias for 'begmode uppercase'
                self.indicators["uppercasebeg"] = dots_to_braille(tokens[1])
            case "endmode":
                self.indicators[tokens[1] + "end"] = dots_to_braille(tokens[2])
            case "endcaps":  # alias for 'endmode caps'
                self.indicators["capsend"] = dots_to_braille(tokens[1])

            case "letsign":  # set letter sign indicator
                self.indicators["letsign"] = dots_to_braille(tokens[1])
            case "nocontractsign":  # only used for UEB (generally)
                self.indicators["nocontractsign"] = dots_to_braille(tokens[1])
            case "numsign":
                self.indicators["numsign"] = dots_to_braille(tokens[1])
            case "nonumsign":
                self.indicators["nonumsign"] = dots_to_braille(tokens[1])

            case "numericnocontchars":
                self.chargroups["_NUMNOCONT"] += tokens[1].split()
            case "numericmodechars":
                self.chargroups["_NUMMODE"] += tokens[1].split()

            # special symbol opcodes
            case "decpoint":
                self.specialsymbols["decpoint"] = (
                    tokens[1],
                    dots_to_braille(tokens[2]),
                )
            case "hyphen":
                self.specialsymbols["hyphen"] = (tokens[1], dots_to_braille(tokens[2]))

            # pretranslation opcodes
            case "correct":
                self.rules["pretrans"].append(
                    MapRule(tokens[1], tokens[2])
                )  # FIXME: 'correct' opcode liblouis syntax

            # translation opcodes
            case "always":
                self.rules["urgent"].append(
                    MapRule(
                        tokens[1],
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )

            case "word":  # match if surrounded by whitespace / punctuation (only space and period for our use case)
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"(?=[\.\s])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "joinword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"[\.\s](?=\w)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "lowword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\s)" + tokens[1] + r"(?=\s)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "sufword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"(?=[\.\s\w])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "prfword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s\w])" + tokens[1] + r"(?=[\.\s])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "begword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"(?=\w)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "begmidword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s\w])" + tokens[1] + r"(?=\w)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "midword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\w)" + tokens[1] + r"(?=\w)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "midendword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\w)" + tokens[1] + r"(?=[\.\s\w])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "endword":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\w)" + tokens[1] + r"(?=[\s\.])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "partword":
                self.rules["early"].append(
                    MapRule(
                        r"((?<=\w)" + tokens[1] + "|" + tokens[1] + r"(?=\w))",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "prepunc":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"(?=[\.]*\w)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "postpunc":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\w[\.]*)" + tokens[1] + r"(?=[\.\s])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "begnum":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=[\.\s])" + tokens[1] + r"(?=\d)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "midnum":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\d)" + tokens[1] + r"(?=\d)",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )
            case "endnum":
                self.rules["early"].append(
                    MapRule(
                        r"(?<=\d)" + tokens[1] + r"(?=[\.\s])",
                        tokens[1] if tokens[2] == "=" else dots_to_braille(tokens[2]),
                    )
                )

            # context and multipass opcodes  (DEPRECATED!!)
            # case "context":
            #    self.rules["pass1"].append(LouisRule(tokens[1], tokens[2]))
            # case "pass2" | "pass3" | "pass4":
            #    self.rules[tokens[0]].append(LouisRule(tokens[1], tokens[2]))

            # match opcode
            case "match":
                # FIXME: liblouis to regex translation; see MatchRule in Rules.py
                pass
                # self.rules["pass1"].append(MatchRule((tokens[1], tokens[2], tokens[3]), tokens[4]))

            # miscellaneous opcodes
            case "undefined":  # set character to be used for untranslatable text
                self.indicators["undefined"] = tokens[
                    1
                ]  # don't translate to braille (obviously)
            case "capsmodechars":  # add characters that will not automatically terminate uppercase mode
                self.chargroups["_CAPSMODE"] += tokens[1].split()

            # not implemented opcodes; log warning and ignore. most of these are for back translation purposes,
            # for braille applications not relevant to our simple sentence format, or just deprecated.
            case (
                "display"
                | "litdigit"
                | "grouping"
                | "largesign"
                | "comprl"
                | "comp6"
                | "nocont"
                | "multind"
                | "swapcd"
                | "swapdd"
                | "swapcc"
                | "noletsign"
                | "noletsignbefore"
                | "noletsignafter"
                | "midendnumericmodechars"
                | "emphclass"
                | "begemph"
                | "endemph"
                | "noemphchars"
                | "emphletter"
                | "begemphword"
                | "endemphword"
                | "emphmodechars"
                | "begemphphrase"
                | "endemphphrase"
                | "lenemphphrase"
                | "begcomp"
                | "endcomp"
                | "capsnocont"
                | "replace"
                | "repeated"
                | "repword"
                | "rependword"
                | "syllable"
                | "contraction"
                | "exactdots"
                | "joinnum"
                | "after"
                | "before"
                | "seqdelimiter"
                | "seqbeforechars"
                | "seqafterchars"
                | "seqafterpattern"
                | "context"  # here onward are deprecated opcodes using liblouis subop syntax (OoS)
                | "pass2"
                | "pass3"
                | "pass4"
            ):
                logging.warning(
                    f"Unimplemented opcode {tokens[0]} used in table {self.file} or an include thereof"
                )

    def translate(self, text: str) -> list[tuple[HalfCell, HalfCell]]:
        # quick and nasty uppercase handling; all that's required for our use case but not particularly classy
        text = "".join(
            self.indicators["uppercaseletter"] + c
            if c in self.chargroups["uppercase"]
            else c
            for c in text
        )

        # pretranslation step
        if self.rules["pretrans"]:
            for rule in self.rules["pretrans"]:
                text, self.variables = rule(text, self.chargroups, self.variables)

        # slight deviation from liblouis translation; handle priority rules before any passes
        if self.rules["urgent"]:
            for rule in self.rules["urgent"]:
                text, self.variables = rule(text, self.chargroups, self.variables)

        if self.rules["early"]:
            for rule in self.rules["early"]:
                text, self.variables = rule(text, self.chargroups, self.variables)

        # first pass
        if self.rules["pass1"]:
            for rule in self.rules["pass1"]:
                text, self.variables = rule(text, self.chargroups, self.variables)
        # reset variables between passes
        self.variables = [0] * 50

        # second pass
        if self.rules["pass2"]:
            for rule in self.rules["pass2"]:
                text, self.variables = rule(text, self.chargroups, self.variables)
        self.variables = [0] * 50

        # third pass
        if self.rules["pass3"]:
            for rule in self.rules["pass3"]:
                text, self.variables = rule(text, self.chargroups, self.variables)
        self.variables = [0] * 50

        # fourth pass
        if self.rules["pass4"]:
            for rule in self.rules["pass4"]:
                text, self.variables = rule(text, self.chargroups, self.variables)
        self.variables = [0] * 50

        # translate any remaining untranslated characters
        if self.rules["charrules"]:
            for rule in self.rules["charrules"]:
                text, self.variables = rule(text, self.chargroups, self.variables)

        # handle decpoint and hyphen
        if self.specialsymbols["decpoint"][0] in text:
            text = re.sub(*self.specialsymbols["decpoint"], text)
        if self.specialsymbols["hyphen"][0] in text:
            text = re.sub(*self.specialsymbols["hyphen"], text)

        # clean up any missed characters using undefined character from tables
        text = "".join(
            c if is_braille(c) else self.indicators["undefined"] for c in text
        )

        # translate to HalfCells and return
        return braille_to_halfcells(text)


# Used in _translate_escapes to convert a few Liblouis escape sequences missing from python to intended characters.
# Format is best understood as the first two arguments to re.sub
_escapes = [
    (re.compile(r"\\s"), " "),
    (re.compile(r"\\e"), "\x1B"),
    (re.compile(r"\\x...."), lambda m: chr(int(str(m[0][-4:]), 16))),
    (re.compile(r"\\y....."), lambda m: chr(int(str(m[0][-5:]), 16))),
    (re.compile(r"\\z........"), lambda m: chr(int(str(m[0][-8:]), 16))),
]


def translate_escapes(text: str) -> str:
    """
    Translates escape sequences in a string from the liblouis table format to the intended character.
    """
    for e in _escapes:
        text = re.sub(*e, text)

    # use str.replace for \\ because python regex module was designed to torment me personally
    text.replace("\\\\", "\\")
    return text


if __name__ == "__main__":
    t = BrailleTranslator()
    print(t.translate("The quick brown fox jumps over the lazy dog.", False))
    print(t.translate("The quick brown fox jumps over the lazy dog.", True))
