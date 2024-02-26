"""
A series of classes designed to encode the rules for Braille translation.
"""
import re
from typing import override


class MapRule:
    """
    Generic class for rules that map a (series of) character(s) to braille.
    The match parameter can be any valid regular expression.
    """

    def __init__(self, match: str, replace: str):
        self.match = re.compile(re.escape(match))  # use compiled regex for performance
        self.replace = replace

    def __call__(
        self, text: str, chargroups: dict[str, list[str]], variables: list[int]
    ) -> tuple[str, list[int]]:
        return re.sub(self.match, self.replace, text), variables


class CharacterRule(MapRule):
    @override
    def __init__(self, match: str, replace: str):
        assert len(match) == 1
        super().__init__(match, replace)


class MatchRule(MapRule):
    """
    Class for rules created with the match opcode. These classes require information about a certain character class
    that may not be complete when the object is instantiated. Thus, the regex is not created until the object is called
    for the first time. The syntax for these rules is not equivalent to that used for LouisRule objects.
    """

    @override
    def __init__(self, match: tuple[str, str, str], replace: str):
        self.match = None
        self.to_match = match  # NB: in this case, match is of the format (prefix, chars, postfix). See liblouis docs.
        self.replace = replace

    # List of compiled regex patterns and substituted strings used to translate from match subop syntax to regex.
    # Implemented as a class attribute in order to reduce compile time; it's the same for all instances
    # NOTE: due to regex limitations, ! is only valid in the context ![Aa], !a, !%_ and similar patterns.
    match_to_regex = [  # no type signature cause i'm mixing tuple[re.Pattern,str] and tuple[re.Pattern,func] >w<
        (re.compile(r"^-$"), ".*"),
        (re.compile(r"(?<=!\[)\w+(?=])"), lambda m: f"[^{m[0]}]"),
        (re.compile(r"(?<=!)\w"), lambda m: f"[^{m[0]}]"),
    ]

    # Map from % syntax character shortcodes to full names. Omit unimplemented shortcodes (~<>).
    char_attributes = {
        "_": "space",
        "#": "digit",
        "a": "letter",
        "u": "uppercase",
        "l": "lowercase",
        ".": "punctuation",
        "$": "sign",
    }

    @override
    def __call__(
        self, text: str, chargroups: dict[str, list[str]], variables: list[int]
    ) -> tuple[str, list[int]]:
        if not self.match:
            # translate to_match:
            for i in self.match_to_regex:
                self.to_match = tuple(re.sub(*i, re.escape(x)) for x in self.to_match)

            # handle %group and !%group syntax
            self.to_match = tuple(
                re.sub(
                    r"(?<=[^!]%)(\[.+]|.)",
                    lambda m: f"[{''.join(chargroups[self.char_attributes[m.group(0)]])}"
                    if len(m.group(0)) == 1
                    else "["
                    + "".join(
                        "".join(chargroups[self.char_attributes[i]])
                        for i in m.group(0)[1:-1]
                    )
                    + "]",
                    m,
                )
                for m in self.to_match
            )
            self.to_match = tuple(
                re.sub(
                    r"!%(\[.+]|.)",
                    lambda m: f"[^{''.join(chargroups[self.char_attributes[m.group(0)]])}"
                    if len(m.group(0)) == 1
                    else "[^" + "".join(
                        "".join(chargroups[self.char_attributes[i]]) for i in m.group(0)[1:-1]) + "]",
                    m)
                for m in self.to_match
            )

            self.match = re.compile(
                "(?<=" + self.to_match[0] + ")"
                + self.to_match[1]
                + "(?=" + self.to_match[2] + ")"
            )

        return re.sub(self.match, self.replace, text), variables


# DEPRECATED
"""
class LouisRule(MapRule):
    @override
    def __init__(self, test: str, action: str):
        self.test = test
        self.action = action

    @override
    def __call__(self, text: str, chargroups: dict[str, list[str]], variables: list[int]) -> tuple[str, list[int]]:
        # Liblouis suboperand code is too complex to translate to regex, so implement it manually.
        # NB: this is a very pared-back version of the Liblouis grammar. Only absolutely necessary features are
        # currently implemented.
        for cursor in range(len(text)):
            ...

        return text, variables

    def _match(self, text: str, chargroups: dict[str, list[str]], variables: list[int]) -> bool:
        ...
"""


# class PretransRule(LouisRule):
#    """
#    Class for rules that translate from text to text, used in the pretranslation step.
#    These can always accept Liblouis suboperands, so the class inherits from LouisRule instead of MapRule.
#    """
