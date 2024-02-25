"""
A series of classes designed to encode the rules for Braille translation.
"""
import re
from typing import override

from .. import Braille
HalfCell = Braille.HalfCell  # FIXME: figure out relative imports


class MapRule:
    """
    Generic class for rules that map a (series of) character(s) to braille.
    The match parameter can be any valid regular expression.
    """
    def __init__(self, match: str, replace: str):
        self.match = re.compile(match)  # use compiled regex for performance
        self.replace = replace

    def __call__(self, text: str, chargroups: dict[str, list[str]]) -> str:
        return re.sub(self.match, self.replace, text)


class CharacterRule(MapRule):
    @override
    def __init__(self, match: str, replace: str):
        assert len(match) == 1
        # assert len(replace) == 1  FIXME: possibly not actually a requirement? check liblouis spec
        super().__init__(match, replace)


class ClassRule(MapRule):
    """
    Class for rules that require information about a certain character class that may not be complete when the object
    is instantiated. Thus, the regex is not created until the object is called for the first time. The class is encoded
    into the regex string as ;classname; and replaced with regex that matches any character in the class.
    """
    @override
    def __init__(self, match: str, replace: str):
        self.replace = replace
        self.to_match = match
        self.match = None

    @override
    def __call__(self, text: str, chargroups: dict[str, list[str]]) -> str:
        if not self.match:
            # TODO: handle ClassRule run-time class substitution
            raise NotImplementedError

        super().__call__(text, chargroups)


class MatchRule(ClassRule):
    """
    Class for rules created with the match opcode. These rules can be compiled to regex at run-time, just as with the
    above ClassRules, but will require an extra translation step to convert from Liblouis pattern expressions to regex.
    """
    @override
    def __init__(self, match: tuple[str, str, str], replace: str):
        self.match = None
        self.to_match = match  # NB: in this case, match is of the format (prefix, chars, postfix). See liblouis docs.
        self.replace = replace

    @override
    def __call__(self, text: str, chargroups: dict[str, list[str]]) -> str:
        if not self.match:
            # TODO: handle MatchRule run-time regex translation and compilation
            raise NotImplementedError

        return re.sub(self.match, self.replace, text)


class LouisRule(MapRule):
    """
    Class for rules that match and/or replace using Liblouis suboperand code.
    """
    @override
    def __init__(self, match: str, replace: str):
        self.match = match
        self.replace = replace

    @override
    def __call__(self, text: str, chargroups: dict[str, list[str]]) -> str:
        # TODO: implement louis suboperand matching
        raise NotImplementedError


class PretransRule(LouisRule):
    """
    Class for rules that translate from text to text, used in the pretranslation step.
    These can always accept Liblouis suboperands, so the class inherits from LouisRule instead of MapRule.
    """
