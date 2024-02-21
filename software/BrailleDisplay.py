from enum import IntEnum, Enum


class BrailleDisplay:
    NUM_CELLS = 8

    class BrailleCell:
        WHEEL_STATES = 8  # number of positions a wheel can be in

        class Direction(IntEnum):
            UP = 1
            DOWN = -1

        Wheel = Enum("Wheel", ["LEFT", "RIGHT"])

        def __init__(self):
            self._l_wheel_pos = 0  # set initial positions of left and right wheels
            self._r_wheel_pos = 0

        def display(self, braille: str):
            """
            Displays a single braille character on the cell.
            @param braille: The character to be displayed.
            """

            raise NotImplementedError

        def _rotate(self, wheel: Wheel, direction: Direction):
            """
            Rotates one of the two wheels that comprise the display cell.
            @param wheel: Either Wheel.LEFT or Wheel.RIGHT
            @param direction: Either Direction.UP or Direction.DOWN
            """

            raise NotImplementedError

    def __init__(self):
        self.cells = [self.BrailleCell() for _ in range(self.NUM_CELLS)]

    def __enter__(self):
        # No point clearing unless we can detect initial positions of the wheels
        pass

    def __exit__(self):
        # Ensure clear on exit to prevent misaligned wheels on future launch
        self.clear()

    def display(self, braille: str):
        if len(braille) > self.NUM_CELLS:
            # TODO: handle braille longer than display
            raise ValueError("Braille string too long for display: " + braille)
        else:
            braille += "⠀" * (self.NUM_CELLS - len(braille))  # pad string with empty braille character
            for i in range(self.NUM_CELLS):
                self.cells[i].display(braille[i])

    def clear(self):
        self.display("⠀" * self.NUM_CELLS)


if __name__ == "__main__":
    with BrailleDisplay() as d:
        d.display("⠁⠏⠏⠇⠑")