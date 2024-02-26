from gpiozero import OutputDevice
from time import sleep
import os

os.environ["GPIOZERO_PIN_FACTORY"] = os.environ.get("GPIOZERO_PIN_FACTORY", "lgpio")

Seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

GEAR_RATIO = 1
DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
FULL_ROTATION = 500.0  # The total number of steps to complete a rotation
DEGREE_PER_ROTATION = 360.0 / FULL_ROTATION
MID_OFFSET = 22.5  # the offset to align all the pips to face up

StepCount = 8


class Stepper:
    CW = -1
    CCW = 1

    """Constructor"""

    def __init__(
        self,
        motor_pins,
    ):
        self.motor_pins = [OutputDevice(pin) for pin in motor_pins]  # Control pins

    def setStep(self, w1, w2, w3, w4):
        new = [w1, w2, w3, w4]
        for pin in range(len(self.motor_pins)):
            if self.motor_pins[pin].is_active:
                if new[pin] == 0:
                    self.motor_pins[pin].off()
            else:
                if new[pin] == 1:
                    self.motor_pins[pin].on()

    def forward(self, delay, steps):
        for i in range(steps):
            for j in range(StepCount):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                sleep(delay)

    def backward(self, delay, steps):
        for i in range(steps):
            for j in reversed(range(StepCount)):
                self.setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
                sleep(delay)

    def movement(self, steps, direction: bool):
        """This method encapsulates the movement of the b stepper motor
        @params : steps ( int from 0 to 7 ) specifying the number of steps to turn
                  direction: either False for back or True for front
        returns True on completetion"""

        step_angle = (
            (steps) * 45 + MID_OFFSET
        )  # 22.5 This is the offset to always align the pip to the middle
        no_of_steps = int(step_angle // DEGREE_PER_ROTATION)
        if direction:
            self.forward(DELAY, no_of_steps)
        else:
            self.backward(DELAY, no_of_steps)
        return True


if __name__ == "_main_":
    while True:
        delay = input("Time Delay (ms)?")
        steps = input("How many steps forward? ")
        stepper = Stepper([18, 13, 16, 15])
        stepper.forward(int(delay) / 1000.0, int(steps))
        steps = input("How many steps backwards? ")
        stepper.backward(int(delay) / 1000.0, int(steps))
