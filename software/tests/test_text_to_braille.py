from text_to_braille import BrailleTranslator, braille_to_halfcells


class TestTextToBraille:
    tl = BrailleTranslator()

    def test_uncontracted(self):
        assert self.tl.translate("the", False) == braille_to_halfcells("⠞⠓⠑")

    def test_contracted(self):
        assert self.tl.translate("the", True) == braille_to_halfcells("⠮")

    def test_extreme(self):
        assert (self.tl.translate("Sphinx of black quartz, judge my vow", False)
                == braille_to_halfcells("⠠⠎⠏⠓⠊⠝⠭⠀⠕⠋⠀⠃⠇⠁⠉⠅⠀⠟⠥⠁⠗⠞⠵⠂⠀⠚⠥⠙⠛⠑⠀⠍⠽⠀⠧⠕⠺"))
