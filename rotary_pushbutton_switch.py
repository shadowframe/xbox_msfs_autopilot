# SPDX-License-Identifier: MIT
import time
import board
import digitalio
import rotaryio
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)


class Encoder_Keycode():
    Encoders = None

    def __init__(self, encoder_keycode_map):
        self.Encoders = encoder_keycode_map

    def update(self):
        for enc in self.Encoders:
            position = enc["encoder"].position
            last_pos = enc["last_pos"]
            if position > last_pos:
                k = enc["clock_wise"]
                if "clock_wise3" in enc:
                    k2 = enc["clock_wise2"]
                    k3 = enc["clock_wise3"]
                    keyboard.press(k, k2, k3)
                    time.sleep(0.2)
                    keyboard.release(k, k2, k3)
                elif "clock_wise2" in enc:
                    k2 = enc["clock_wise2"]
                    keyboard.press(k, k2)
                    time.sleep(0.2)
                    keyboard.release(k, k2)
                else:
                    keyboard.press(k)
                    time.sleep(0.2)
                    keyboard.release(k)
                enc["last_pos"] = position
            elif position < last_pos:
                k = enc["anti_clock_wise"]
                if "anti_clock_wise3" in enc:
                    k2 = enc["anti_clock_wise2"]
                    k3 = enc["anti_clock_wise3"]
                    keyboard.press(k, k2, k3)
                    time.sleep(0.2)
                    keyboard.release(k, k2, k3)
                elif "anti_clock_wise2" in enc:
                    k2 = enc["anti_clock_wise2"]
                    keyboard.press(k, k2)
                    time.sleep(0.2)
                    keyboard.release(k, k2)
                else:
                    keyboard.press(k)
                    time.sleep(0.2)
                    keyboard.release(k)
                enc["last_pos"] = position


class Button_Keycode():
    Buttons = None

    def __init__(self, pin_keycode_map):
        self.Buttons = pin_keycode_map
        for btn in self.Buttons:
            pin = digitalio.DigitalInOut(btn["pin"])
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP
            btn["debouncer"] = Debouncer(pin, interval=0.005)

    def update(self):
        for btn in self.Buttons:
            debounced_pin = btn["debouncer"]
            debounced_pin.update()
            if debounced_pin.fell:
                if "keycode3" in btn:
                    keyboard.press(btn["keycode"], btn["keycode2"], btn["keycode3"])
                elif "keycode2" in btn:
                    keyboard.press(btn["keycode"], btn["keycode2"])
                else:
                    keyboard.press(btn["keycode"])
            elif debounced_pin.rose:
                if "keycode3" in btn:
                    keyboard.release(btn["keycode"], btn["keycode2"], btn["keycode3"])
                elif "keycode2" in btn:
                    keyboard.release(btn["keycode"], btn["keycode2"])
                else:
                    keyboard.release(btn["keycode"])


class switch:
    def __init__(self, port, key1, key2):  # This will setup our desired Button and bind it to uC!
        self.switch = digitalio.DigitalInOut(port)  # Make a psychical Anchorn a INPUT!
        self.switch.switch_to_input(pull=digitalio.Pull.UP)  # Make it HIGH!
        self.key1 = key1
        self.key2 = key2
        self.state = True  # This will prevent us from unnecesary repeting
    def test_switch(self):  # This will be testing state of Switch
        if self.switch.value != self.state:
            if self.switch.value == False:  # This will execute if switch is ON!
                keyboard.press(self.key1)
                keyboard.release_all()
                time.sleep(400/1000)
                self.state = False
            else: #This will execute if switch is OFF!
                keyboard.press(self.key2)
                keyboard.release_all()
                time.sleep(400/1000)
                self.state = True

Buttons = Button_Keycode([
    # Heading Bug Todo
    {"pin": board.GP2, "keycode": Keycode.F9},
    # Altitude Push Todo
    {"pin": board.GP5, "keycode": Keycode.F9},
    # Altitude ARM !TOGGLE VERTICAL SPEED
    {"pin": board.GP6, "keycode": Keycode.CONTROL, "keycode2": Keycode.ALT, "keycode3": Keycode.V},
    # Flight Director
    {"pin": board.GP7, "keycode": Keycode.CONTROL, "keycode2": Keycode.F},
    # Vertical Speed Down
    {"pin": board.GP8, "keycode": Keycode.CONTROL, "keycode2": Keycode.END},
    # Vertical Speed Up
    {"pin": board.GP9, "keycode": Keycode.CONTROL, "keycode2": Keycode.HOME},
    # ALT Hold !There are two altitude hold assignments at the settings, use the unassigned to ALT-T
    {"pin": board.GP10, "keycode": Keycode.ALT, "keycode2": Keycode.T},
    # APROACH Hold
    {"pin": board.GP11, "keycode": Keycode.CONTROL, "keycode2": Keycode.A},
    # NAV GPS Mode
    {"pin": board.GP12, "keycode": Keycode.CONTROL, "keycode2": Keycode.N},
    # HDG Mode Todo !Set Heading Hold STRG-U
    {"pin": board.GP13, "keycode": Keycode.CONTROL, "keycode2": Keycode.U},
    # FLC Flight Level Change ... Todo
    {"pin": board.GP14, "keycode": Keycode.ALT, "keycode2": Keycode.L},
    # CDI Todo
    {"pin": board.GP15, "keycode": Keycode.ALT, "keycode2": Keycode.Z},
    # Autopilot ON/OFF !Change Keyboard Shortcut in the settings (Normaly On AND Off) from ON to TOGGLE
    # {"pin": board.GP16, "keycode": Keycode.Y},
    {"pin": board.GP17, "keycode": Keycode.F17},
    {"pin": board.GP18, "keycode": Keycode.F18},
    {"pin": board.GP19, "keycode": Keycode.F19},
    {"pin": board.GP20, "keycode": Keycode.INSERT},
    {"pin": board.GP21, "keycode": Keycode.DELETE},
    {"pin": board.GP22, "keycode": Keycode.HOME},
    {"pin": board.GP26, "keycode": Keycode.END},
    {"pin": board.GP27, "keycode": Keycode.PAGE_UP},
    {"pin": board.GP28, "keycode": Keycode.PAGE_DOWN},
])

Encoders = Encoder_Keycode([
    # Bottom Encoder Heading Bug
    {"encoder": rotaryio.IncrementalEncoder(board.GP0, board.GP1), \
     "last_pos": 0, "clock_wise": Keycode.CONTROL, "clock_wise2": Keycode.INSERT, "anti_clock_wise": Keycode.CONTROL,
     "anti_clock_wise2": Keycode.DELETE},
    # Top Encoder Altitude
    {"encoder": rotaryio.IncrementalEncoder(board.GP3, board.GP4), \
     "last_pos": 0, "clock_wise": Keycode.CONTROL, "clock_wise2": Keycode.PAGE_DOWN, "anti_clock_wise": Keycode.CONTROL,
     "anti_clock_wise2": Keycode.PAGE_UP},
])
# def myfunction():
#     print("Hallo Jan12")
#     time.sleep(1)

s1 = switch(board.GP16,Keycode.B,Keycode.C)

while True:
    Encoders.update()
    Buttons.update()
    s1.test_switch()
#     myfunction()

# Connect to board with osx
# ls /dev/tty.*
# screen /dev/tty.board_name 115200
