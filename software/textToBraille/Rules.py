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
    def __init__(self, match: str, braille: str):
        self.match = re.compile(match)  # use compiled regex for performance
        self.braille = braille

    def __call__(self, text, chargroups):
        re.sub(self.match, self.braille, text)


class CharacterRule(MapRule):
    @override
    def __init__(self, match: str, braille: str):
        assert len(match) == 1
        assert len(braille) == 1
        super().__init__(match, braille)


class ClassRule(MapRule):
    """
    Class for rules that require information about a certain character class that may not be complete when the object
    is instantiated. Thus, the regex is not created until the object is called for the first time. The class is encoded
    into the regex string as ;classname; and replaced with regex that matches any character in the class.
    """
    @override
    def __init__(self, match: str, braille: str):
        self.braille = braille
        self.matchstr = match
        self.match = None

    @override
    def __call__(self, text, chargroups):
        if not self.match:
            # TODO: handle ClassRule run-time class substitution
            raise NotImplementedError

        super().__call__(text, chargroups)


class PretransRule(MapRule):
    """
    Class for rules that translate from text to text, used in the pretranslation step.
    """
