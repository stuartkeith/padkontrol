#!/usr/bin/env python

import padkontrol as pk
import rtmidi
from rtmidi.midiutil import open_midioutput, open_midiinput

# should be named 'padKONTROL 1 CTRL' or similar.
OUTPUT_MIDI_PORT = 2
# should be named 'padKONTROL 1 PORT A' or similar
INPUT_MIDI_PORT = 1


midi_out, _ = open_midioutput(
    OUTPUT_MIDI_PORT,
    api=rtmidi.API_UNIX_JACK,
    client_name="padkontrol",
    port_name="MIDI Out")


def send_sysex(sysex):
    midi_out.send_message(sysex)


class PadKontrolPrint(pk.PadKontrolInput):
    def on_pad_down(self, pad, velocity):
        print 'pad #%d down, velocity %d/127' % (pad, velocity)

    def on_pad_up(self, pad):
        print 'pad #%d up' % pad

    def on_button_down(self, button):
        if button == pk.BUTTON_FLAM:
            print 'flam button down'
        else:
            print 'button #%d down' % button

    def on_button_up(self, button):
        if button == pk.BUTTON_MESSAGE:
            print 'message button up'
        else:
            print 'button #%d up' % button

    def on_knob(self, knob, value):
        print 'knob #%d value = %d' % (knob, value)

    def on_rotary_left(self):
        print 'rotary turned left'

    def on_rotary_right(self):
        print 'rotary turned right'

    def on_x_y(self, x, y):
        print 'x/y pad (x = %d, y = %d)' % (x, y)


send_sysex(pk.SYSEX_NATIVE_MODE_OFF)

raw_input('Press enter to enable native mode.')

send_sysex(pk.SYSEX_NATIVE_MODE_ON) # must be sent first
send_sysex(pk.SYSEX_NATIVE_MODE_ENABLE_OUTPUT)
send_sysex(pk.SYSEX_NATIVE_MODE_INIT) # must be sent after SYSEX_NATIVE_MODE_ON
send_sysex(pk.SYSEX_NATIVE_MODE_TEST) # displays 'YES' on the LED

raw_input('Press enter to display blinking numbers.')

send_sysex(pk.led('123', pk.LED_STATE_BLINK))

raw_input('Press enter to display a greeting.')

welcome_message = pk.string_to_sysex('Hi ')

send_sysex(pk.led(welcome_message))

raw_input('Press enter to see the PROG CHANGE button flash once.')

send_sysex(pk.light_flash(pk.BUTTON_PROG_CHANGE, 0.5))

raw_input('Press enter to see pad #4 blink.')

send_sysex(pk.light(4, pk.LIGHT_STATE_BLINK))

raw_input('Press enter to light up the KNOB 1 ASSIGN button.')

send_sysex(pk.light(pk.BUTTON_KNOB_1_ASSIGN, True))

raw_input('Press enter to turn off pad #4 and the KNOB 1 ASSIGN lights.')

send_sysex(pk.light(4, False))
send_sysex(pk.light(pk.BUTTON_KNOB_1_ASSIGN, pk.LIGHT_STATE_OFF))

raw_input('Press enter to turn on multiple lights with one message.')

send_sysex(pk.light_group(welcome_message, {
        0: True,
        1: True,
        2: True,
        4: True,
        6: True,
        8: True,
        9: True,
        10: True,
        pk.BUTTON_X: True,
        pk.BUTTON_Y: True,
        pk.BUTTON_PEDAL: True,
        pk.BUTTON_NOTE_CC: True,
        pk.BUTTON_SW_TYPE: True,
        pk.BUTTON_REL_VAL: True,
        pk.BUTTON_VELOCITY: True,
        pk.BUTTON_PORT: True
    }))

raw_input('Press enter to demonstrate input handling (then enter again to exit this example).')

midi_in, _ = open_midiinput(
    INPUT_MIDI_PORT,
    api=rtmidi.API_UNIX_JACK,
    client_name="padkontrol",
    port_name="MIDI In")

pk_print = PadKontrolPrint()

def midi_in_callback(message, data):
    sysex_buffer = []
    for byte in message[0]:
        sysex_buffer.append(byte)

        if (byte == 0xF7):
            pk_print.process_sysex(sysex_buffer)
            del sysex_buffer[:] # empty list

midi_in.ignore_types(False, False, False)
midi_in.set_callback(midi_in_callback)

raw_input('Press enter to exit')

send_sysex(pk.SYSEX_NATIVE_MODE_OFF)

midi_in.close_port()
midi_out.close_port()
