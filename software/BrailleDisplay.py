from enum import IntEnum, Enum
from Braille import HalfCell, BRAILLE_DICT
import Pip_Rotator as PR


Wheel = Enum("Wheel", ["LEFT", "RIGHT"])


class BrailleDisplay:
    NUM_CELLS = 8

    class BrailleCell:
        def __init__(self):
            self._l_wheel_pos = HalfCell.NO_DOT
            self._r_wheel_pos = HalfCell.NO_DOT

        def display(self, text: str):
            """
            Displays a single braille character on the cell.
            @param braille: The character to be displayed.
            """

            for char in text:
                if char not in BRAILLE_DICT:
                    raise ValueError("Invalid braille character: " + char)
                else:
                    l_wheel, r_wheel = BRAILLE_DICT[char]
                    self._rotate(Wheel.LEFT, l_wheel)
                    self._rotate(Wheel.RIGHT, r_wheel)

        def _rotate(self, wheel: Wheel, half_cell: HalfCell):
            """
            Rotates one of the two wheels that comprise the display cell.
            @param wheel: Either Wheel.LEFT or Wheel.RIGHT
            @param direction: Either Direction.UP or Direction.DOWN
            """

            pos = self.get_pos(wheel)
            # some GPIO magic here
            if pos == half_cell:
                # no need to rotate
               pass 
            elif pos < half_cell:
                # rotate down
                # DIRECTION_DOWN
                PR.movement ( (half_cell - pos), True)

            else:
                # rotate up
                # DIRECTION_UP
                PR.movement((pos - half_cell), False)

            # updating the position after rotation
            if wheel == Wheel.LEFT:
                self._l_wheel_pos = half_cell
            else:
                self._r_wheel_pos = half_cell

        def get_pos(self, wheel: Wheel) -> HalfCell:
            """
            Returns the current position of the specified wheel.
            @param wheel: Either Wheel.LEFT or Wheel.RIGHT
            @return: The current position of the wheel.
            """
            return self._l_wheel_pos if wheel == Wheel.LEFT else self._r_wheel_pos

    def __init__(self):
        self.cells = [self.BrailleCell() for _ in range(self.NUM_CELLS)]

    def __enter__(self):
        # No point clearing unless we can detect initial positions of the wheels
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure clear on exit to prevent misaligned wheels on future launch
        self.clear()

    def display(self, text: str):
        if len(text) > self.NUM_CELLS:
            # TODO: handle braille longer than display
            raise ValueError("Braille string too long for display: " + text)
        else:
            for i in range(0, len(text)):
                self.cells[i].display(text[i])
                print(f'Cell {i} displayed {self.cells[i]._l_wheel_pos} {self.cells[i]._r_wheel_pos}')

    def clear(self):
        self.display(" " * self.NUM_CELLS)


if __name__ == "__main__":
    with BrailleDisplay() as d:
        d.display("apple")
