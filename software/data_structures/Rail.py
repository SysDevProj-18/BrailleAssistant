from gpiozero import OutputDevice
from time import sleep
import os
from .Wheel import Wheel

os.environ["GPIOZERO_PIN_FACTORY"] = os.environ.get("GPIOZERO_PIN_FACTORY", "lgpio")

GEAR_RATIO = 1
DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
DEGREE_PER_ROTATION = 1.8
GAP_LEFT_RIGHT = 2.0
INTER_CELL_GAP = 1 # number of steps for the small gap
MULTI_CELL_GAP = 0.5 # number of steps for a big gap

class Rail:
    def __init__(
        self,
        motor_pins,
    ):
        self.motor_pins = [OutputDevice(pin) for pin in motor_pins]  # Control pins
        self.pos = [0,0] # 0 for left and 1 for right
        self.DIR = OutputDevice(motor_pins[0]) # left motor pin is the direction
        self.STEP = OutputDevice(motor_pins[1]) #right motor pin is the direction
        self.steps = 0



    def move_to(self, pos: int , wheel: Wheel):
        # move forward or backward
        if self.pos != pos:
            print("Moving rail from ", self.pos, " to ", pos)
            if self.pos < pos[0]:
                self.steps = self.step_calculator(pos, wheel, True)
                self._forward(self.steps)

            elif self.pos > pos[0]:
                self.steps = self.step_calculator(pos, wheel, False)
                self._backward(self.steps)

            self.pos[0] = pos
            self.pos[1] = wheel

    def step_calculator(self, pos: int, wheel:Wheel , dir: bool):
        steps = INTER_CELL_GAP
        if dir:
            steps = MULTI_CELL_GAP * (pos[0] - pos)
            steps = steps + INTER_CELL_GAP * abs(wheel - pos[1])

        else :
            steps = MULTI_CELL_GAP * (pos - pos[0])
            steps = steps + INTER_CELL_GAP * abs(wheel - pos[1])
        return steps

    def _forward(self,steps: int):
        self.DIR.on()
        for i in range(int):
            self.STEP.on()
            sleep(DELAY)
            self.STEP.off()
            sleep(DELAY)

    def _backward(self,steps: int):
        self.DIR.off()
        for i in range(int):
            self.STEP.on()
            sleep(DELAY)
            self.STEP.off()
            sleep(DELAY)


if __name__ == "_main_":
    print("Hello World")
