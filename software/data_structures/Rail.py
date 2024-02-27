from gpiozero import OutputDevice
from time import sleep
import os

os.environ["GPIOZERO_PIN_FACTORY"] = os.environ.get("GPIOZERO_PIN_FACTORY", "lgpio")


class Rail:
    def __init__(
        self,
        motor_pins,
    ):
        self.motor_pins = [OutputDevice(pin) for pin in motor_pins]  # Control pins
        self.pos = 0

    def move_to(self, pos: int):
        # move forward or backward
        while self.pos != pos:
            print("Moving rail from ", self.pos, " to ", pos)
            if self.pos < pos:
                self._forward()
                self.pos += 1
            elif self.pos > pos:
                self._backward()
                self.pos -= 1

    def _forward(self):
        # gpio magic
        pass

    def _backward(self):
        # gpio magic
        pass


if __name__ == "_main_":
    print("Hello World")
