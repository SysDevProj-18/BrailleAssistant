from enum import IntEnum, Enum
from Braille import HalfCell, BRAILLE_DICT


Wheel = Enum("Wheel", ["LEFT", "RIGHT"])


class BrailleDisplay:
    NUM_CELLS = 10 # TODO merge this with DISPLAY_SIZE in main

    class BrailleCell:
        def __init__(self):
            self._l_wheel_pos = HalfCell.NO_DOT
            self._r_wheel_pos = HalfCell.NO_DOT

        def display(self, cell: "tuple[HalfCell, HalfCell]"):
            """
            Displays a single braille character on the cell.
            @param braille: The character to be displayed.
            """
            
            l_wheel, r_wheel = cell
            self._rotate(Wheel.LEFT, l_wheel)
            self._rotate(Wheel.RIGHT, r_wheel)

        def _rotate(self, wheel: Wheel, half_cell: HalfCell):
            """
            Rotates one of the two wheels that comprise the display cell.
            @param wheel: Either Wheel.LEFT or Wheel.RIGHT
            @param direction: Either Direction.UP or Direction.DOWN
            """
            # some GPIO magic here
            if self.get_pos(wheel) == half_cell:
                # no need to rotate
               pass 
            elif self.get_pos(wheel) < half_cell:
                # rotate down
                # DIRECTION_DOWN
                # GPIO Magic
               pass 
            else:
                # rotate up
                # DIRECTION_UP
                # GPIO Magic
               pass 
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

    def display(self, braille: "list[tuple[HalfCell, HalfCell]]"):
        if len(braille) > self.NUM_CELLS:
            # TODO: handle braille longer than display
            raise ValueError(f"Braille string too long for display: {braille}")
        else:
            for i in range(0, len(braille)):
                self.cells[i].display(braille[i])
                print(f'Cell {i} displayed {self.cells[i]._l_wheel_pos} {self.cells[i]._r_wheel_pos}')
            for i in range(len(braille), self.NUM_CELLS):
                self.cells[i].display((HalfCell.NO_DOT, HalfCell.NO_DOT))
                print(f'Cell {i} blanked to {self.cells[i]._l_wheel_pos} {self.cells[i]._r_wheel_pos}')

    def clear(self):
        self.display([])


if __name__ == "__main__":
    with BrailleDisplay() as d:
        d.display("apple")
