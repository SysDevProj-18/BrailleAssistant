import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
coil_A_1_pin = 17  # IN1
coil_A_2_pin = 18  # IN2
coil_B_1_pin = 21  # IN3
coil_B_2_pin = 22  # IN4
GEAR_RATIO = 1
DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
FULL_ROTATION = 500.0  # The total number of steps to complete a rotation
DEGREE_PER_ROTATION = 360.0 / FULL_ROTATION
MID_OFFSET = 22.5  # the offset to align all the pips to face up

# adjust if different
StepCount = 8
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

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)


def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def movement(steps, direction):
    """This method encapsulates the movement of the b stepper motor
    @params : steps ( int from 0 to 7 ) specifying the number of steps to turn
              direction: either False for back or True for front
    returns True on completetion"""

    step_angle = (
        steps
    ) * 45 + MID_OFFSET  # 22.5 This is the offset to always align the pip to the middle
    no_of_steps = step_angle // DEGREE_PER_ROTATION
    if direction:
        forward(DELAY, no_of_steps)
    else:
        backwards(DELAY, no_of_steps)
    return True


if __name__ == "_main_":
    while True:
        delay = input("Time Delay (ms)?")
        steps = input("How many steps forward? ")
        forward(int(delay) / 1000.0, int(steps))
        steps = input("How many steps backwards? ")
        backwards(int(delay) / 1000.0, int(steps))
