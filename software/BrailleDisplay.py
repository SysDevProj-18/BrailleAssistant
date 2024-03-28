from data_structures import HalfCell, Stepper, Rail, Wheel

stepper_IN1 = 26
stepper_IN2 = 16
stepper_IN3 = 20
stepper_IN4 = 21

rail_IN1 = 27
rail_IN2 = 17


class BrailleDisplay:
    NUM_CELLS = 10  # TODO merge this with DISPLAY_SIZE in main

    class BrailleCell:
        def __init__(self, stepper: Stepper, rail: Rail, id):
            self._l_wheel_pos = HalfCell.NO_DOT
            self._r_wheel_pos = HalfCell.NO_DOT
            self.stepper = stepper
            self.rail = rail
            self.id = id

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

            pos = self.get_pos(wheel)
            # some GPIO magic here
            if pos == half_cell:
                # no need to rotate
                pass
            elif pos < half_cell:
                # rotate down
                self.rail.move_to(self.id, wheel)
                self.stepper.movement((half_cell - pos), False)
            else:
                # rotate up
                # DIRECTION_UP
                self.rail.move_to(self.id, wheel)
                self.stepper.movement((pos - half_cell), True)

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
        self.stepper = Stepper([stepper_IN1, stepper_IN2, stepper_IN3, stepper_IN4])
        self.rail = Rail([rail_IN1, rail_IN2])
        self.cells = [
            self.BrailleCell(self.stepper, self.rail, i) for i in range(self.NUM_CELLS)
        ]

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
                print(
                    f"Cell {i} displayed {self.cells[i]._l_wheel_pos} {self.cells[i]._r_wheel_pos}"
                )
            for i in range(len(braille), self.NUM_CELLS):
                self.cells[i].display((HalfCell.NO_DOT, HalfCell.NO_DOT))
                print(
                    f"Cell {i} blanked to {self.cells[i]._l_wheel_pos} {self.cells[i]._r_wheel_pos}"
                )
            # return to cell 0
            self.rail.move_to(0, Wheel.LEFT)

    def clear(self):
        self.display([])


if __name__ == "__main__":
    with BrailleDisplay() as d:
        d.display("apple")
