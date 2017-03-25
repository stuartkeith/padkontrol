import math


# button constants
BUTTON_SCENE = 0x10
BUTTON_MESSAGE = 0x11
BUTTON_SETTING = 0x12
BUTTON_NOTE_CC = 0x13
BUTTON_MIDI_CH = 0x14
BUTTON_SW_TYPE = 0x15
BUTTON_REL_VAL = 0x16
BUTTON_VELOCITY = 0x17
BUTTON_PORT = 0x18
BUTTON_FIXED_VELOCITY = 0x19
BUTTON_PROG_CHANGE = 0x1A
BUTTON_X = 0x1B
BUTTON_Y = 0x1C
BUTTON_KNOB_1_ASSIGN = 0x1D
BUTTON_KNOB_2_ASSIGN = 0x1E
BUTTON_PEDAL = 0x1F
BUTTON_ROLL = 0x20
BUTTON_FLAM = 0x21
BUTTON_HOLD = 0x22
BUTTON_PAD = 0X30

# light state constants
LIGHT_STATE_OFF = 0x00
LIGHT_STATE_ON = 0x20
LIGHT_STATE_ONESHOT = 0x40
LIGHT_STATE_BLINK = 0x60

# LED state constants
LED_STATE_ON = 0x00
LED_STATE_BLINK = 0x01

# SYSEX constants
_SYSEX_COMMON = [0xF0, 0x42, 0x40, 0x6E, 0x08]
SYSEX_NATIVE_MODE_ON = _SYSEX_COMMON + [0x00, 0x00, 0x01, 0xF7]
SYSEX_NATIVE_MODE_ENABLE_OUTPUT = _SYSEX_COMMON + [0x3F, 0x2A, 0x00, 0x00,
    0x05, 0x05, 0x05, 0x7F, 0x7E, 0x7F, 0x7F, 0x03, 0x0A, 0x0A, 0x0A, 0x0A,
    0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A,
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C,
    0x0d, 0x0E, 0x0F, 0x10, 0xF7]
SYSEX_NATIVE_MODE_INIT = _SYSEX_COMMON + [0xF0, 0x42, 0x40, 0x6E, 0x08, 0x3F,
    0x0A, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x29, 0x29, 0x29, 0xF7]
# displays YES on LED if native mode is enabled properly
SYSEX_NATIVE_MODE_TEST = _SYSEX_COMMON + [0x22, 0x04, 0x00, 0x59, 0x45, 0x53,
    0xF7]
SYSEX_NATIVE_MODE_OFF = _SYSEX_COMMON + [0x00, 0x00, 0x00, 0xF7]


def string_to_sysex(string):
    """Convert a string to the type required by the PadKontrol.

    string -- the string to convert. Must be 3 characters long.
    """
    if len(string) != 3:
        raise ValueError('String \'%s\' must be 3 characters long' % string)

    return [ord(s) for s in string]

def ensure_sysex(value):
    """Ensure the value is the correct type.

    value -- either a string (will be converted) or a list (will be returned
             unmodified).
    """
    if isinstance(value, basestring):
        return string_to_sysex(value)
    else:
        return value

def light_group(led, lights):
    """Set the LED readout and multiple lights at once.

    led -- either a string or a string converted by string_to_sysex.

    lights -- a dictionary. Specify pad numbers (0 to 15) or button constants
              as keys, and indicate whether the associated light is on or off
              via a truth-y or false-y value. Any missing pads or buttons will
              be turned off.

              In this example, BUTTON_X and pad #6 will be on, and pad #4 will
              be off:

              {
                  BUTTON_X: True,
                  6: True,
                  4: False
              }
    """
    # LED must be reversed
    led = ensure_sysex(led)[::-1]

    group = [0 for i in range(5)]

    for light, value in lights.items():
        if value:
            group_index = light / 7
            remainder = light % 7
            group[group_index] += int(math.pow(2, remainder))

    return _SYSEX_COMMON + [0x3F, 0x0A, 0x01] + group + [0x00] + led + [0xF7]

def light(button_or_pad, light_state):
    """Set the state of the specified button or pad's light.

    button_or_pad -- a button value constant or pad number (0 to 15).

    light_state -- a light state constant or True (on) or False (off).
    """
    if light_state is True:
        light_state = LIGHT_STATE_ON
    elif light_state is False:
        light_state = LIGHT_STATE_OFF

    return _SYSEX_COMMON + [0x01, button_or_pad, light_state, 0xF7]

def light_flash(button_or_pad, duration):
    """Flash the button's light momentarily.

    button_or_pad -- a button value constant or pad number (0 to 15).

    duration -- a number between 0 (9ms) and 1.0 (279ms).
    """
    speed = LIGHT_STATE_ONESHOT + int(30 * duration)

    return light(button_or_pad, speed)

def led(led, led_state=LED_STATE_ON):
    """Set the LED display.

    led -- either a string or a list returned from string_to_sysex.

    led_state -- a LED state constant (default is on)
    """
    led = ensure_sysex(led)

    return _SYSEX_COMMON + [0x22, 0x04, led_state] + led + [0xF7]


class PadKontrolInput:
    """Handle the PadKontrol's output.

    Extend this class and override the on_* methods to respond to PadKontrol
    events. Pass SYSEX data to the process_sysex method to trigger those
    methods.
    """

    def process_sysex(self, sysex):
        """Inspect the SYSEX and call the relevant handler.

        sysex -- a SYSEX message in the form of a list of integers.
                 Must be a fully formed SYSEX message (begins with 0xF0, ends
                 with 0xF7).
        """
        first = sysex[5]
        second = sysex[6]
        third = sysex[7]

        # pad
        if first == 0x45:
            if second >= 64:
                self.on_pad_down(second - 64, third)
            else:
                self.on_pad_up(second)
        # button
        elif first == 0x48:
            if third == 127:
                self.on_button_down(second + 16)
            else:
                self.on_button_up(second + 16)
        # knob
        elif first == 0x49:
            self.on_knob(second, third)
        # rotary encoder
        elif first == 0x43:
            if third == 1:
                self.on_rotary_right()
            else:
                self.on_rotary_left()
        # x/y pad
        elif first == 0x4B:
            self.on_x_y(second, third)
        # invalid SYSEX
        else:
            self.on_invalid_sysex(sysex)

    def on_invalid_sysex(self, sysex):
        raise ValueError("unrecognised SYSEX - %s", sysex)

    def on_pad_down(self, pad, velocity):
        pass

    def on_pad_up(self, pad):
        pass

    def on_button_down(self, button):
        pass

    def on_button_up(self, button):
        pass

    def on_knob(self, knob, value):
        pass

    def on_rotary_left(self):
        pass

    def on_rotary_right(self):
        pass

    def on_x_y(self, x, y):
        pass
