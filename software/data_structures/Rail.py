from gpiozero import OutputDevice
from time import sleep
import os
from .Wheel import Wheel


GEAR_RATIO = 1
DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
DEGREE_PER_ROTATION = 1.8
GAP_LEFT_RIGHT = 2.0
INTER_CELL_GAP = 70  # number of steps for the small gap
MULTI_CELL_GAP = 30  # number of steps for a big gap


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
        return abs(multi_cell_gap) * MULTI_CELL_GAP + abs(inter_gap) * INTER_CELL_GAP

    def _forward(self, steps: int):
        self.motor_pins[0].on()
        for _ in range(steps):
            self.motor_pins[1].on()
            sleep(DELAY)
            self.motor_pins[1].off()
            sleep(DELAY)

    def _backward(self, steps: int):
        self.motor_pins[0].off()
        for _ in range(steps):
            self.motor_pins[1].on()
            sleep(DELAY)
            self.motor_pins[1].off()
            sleep(DELAY)


if __name__ == "_main_":
    print("Hello World")
