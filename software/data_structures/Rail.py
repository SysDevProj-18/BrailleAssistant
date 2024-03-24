from gpiozero import OutputDevice
from constants import Constants
from time import sleep
import os
from .Wheel import Wheel


class Rail:
    def __init__(
        self,
        motor_pins,
    ):
        self.motor_pins = [OutputDevice(pin) for pin in motor_pins]  # Control pins
        self.pos = [0, 0]  # 0 for left and 1 for right
        self.steps = 0

    def move_to(self, pos: int, wheel: Wheel):
        # move forward or backward
        print("Moving rail from ", self.pos, " to ", pos)
        print(f"self.pos = {self.pos}" + " pos = " + f"{pos}")
        if self.pos[0] < pos or self.pos[1] < wheel:
            self.steps = self.step_calculator(pos, wheel, True)
            print("Steps: ", self.steps)
            self._forward(self.steps)

        elif self.pos[0] > pos or self.pos[1] > wheel:
            self.steps = self.step_calculator(pos, wheel, False)
            self._backward(self.steps)

        self.pos[0] = pos
        self.pos[1] = wheel

    def step_calculator(self, pos: int, wheel: Wheel, dir: bool):
        inter_gap = (wheel + pos) - (self.pos[0] + self.pos[1])
        multi_cell_gap = self.pos[0] - pos
        return (
            abs(multi_cell_gap) * Constants.RAIL_MULTI_CELL_GAP
            + abs(inter_gap) * Constants.RAIL_INTER_CELL_GAP
        )

    def _forward(self, steps: int):
        self.motor_pins[0].on()
        for _ in range(steps):
            self.motor_pins[1].on()
            sleep(Constants.RAIL_DELAY)
            self.motor_pins[1].off()
            sleep(Constants.RAIL_DELAY)

    def _backward(self, steps: int):
        self.motor_pins[0].off()
        for _ in range(steps):
            self.motor_pins[1].on()
            sleep(Constants.RAIL_DELAY)
            self.motor_pins[1].off()
            sleep(Constants.RAIL_DELAY)


if __name__ == "_main_":
    print("Hello World")
