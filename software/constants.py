from data_structures import HalfCell


class Constants:
    RAIL_IN1 = 2
    RAIL_IN2 = 3
    RAIL_GEAR_RATIO = 1
    RAIL_DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
    RAIL_DEGREE_PER_ROTATION = 1.8
    RAIL_GAP_LEFT_RIGHT = 2.0
    RAIL_INTER_CELL_GAP = 70  # number of steps for the small gap
    RAIL_MULTI_CELL_GAP = 30  # number of steps for a big gap

    STEPPER_IN2 = 16
    STEPPER_IN3 = 20
    STEPPER_IN4 = 21
    STEPPER_IN1 = 26
    STEPPER_GEAR_RATIO = 1
    STEPPER_DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
    STEPPER_FULL_ROTATION = 500.0  # The total number of steps to complete a rotation
    STEPPER_DEGREE_PER_ROTATION = 360.0 / STEPPER_FULL_ROTATION
    STEPPER_MID_OFFSET = 22.5  # the offset to align all the pips to face up

    STEPPER_STEP_COUNT = 8
    REGULAR_KEYS = list("qwertyuiopasdfghjklzxcvbnm0123456789.:,;!?'\"(){}[]/\\-")
    KEY_SPACE = "space"
    KEY_BACKSPACE_TEXT_ENTRY = "backspace"
    KEY_CLEAR_TEXT_ENTRY = "delete"
    KEY_SUBMIT_TEXT_ENTRY = "enter"
    GAME_MENU_KEYS = ["1", "2"]
    KEY_SPEAK_KEYPRESS_ON = "f2"
    KEY_SPEAK_KEYPRESS_OFF = "f3"
    KEY_SPEAK_STORED = "f4"
    KEY_MICROPHONE = "f5"
    KEY_CAMERA = "f6"
    KEY_GAME = "f7"
    KEY_PREVIOUS_PAGE = "left"
    KEY_NEXT_PAGE = "right"
    KEY_UNCONTRACTED_BRAILLE = "f11"
    KEY_CONTRACTED_BRAILLE = "f12"
    KEY_VOLUME_UP = "pagedown"
    KEY_VOLUME_DOWN = "pageup"
    DISPLAY_SIZE = 10
    BRAILLE_SPACE = (HalfCell.NO_DOT, HalfCell.NO_DOT)

    RAIL_GEAR_RATIO = 1
    RAIL_DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
    RAIL_DEGREE_PER_ROTATION = 1.8
    RAIL_GAP_LEFT_RIGHT = 2.0
    RAIL_INTER_CELL_GAP = 70  # number of steps for the small gap
    RAIL_MULTI_CELL_GAP = 30  # number of steps for a big gap

    STEPPER_GEAR_RATIO = 1
    STEPPER_DELAY = 0.001  # in seconds, lower it to increase the speed of the motor
    STEPPER_FULL_ROTATION = 500.0  # The total number of steps to complete a rotation
    STEPPER_DEGREE_PER_ROTATION = 360.0 / STEPPER_FULL_ROTATION
    STEPPER_MID_OFFSET = 22.5  # the offset to align all the pips to face up

    STEPPER_STEP_COUNT = 8
