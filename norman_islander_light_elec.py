import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


#defining THE class, a heart of device, ritual cannot be done without THIS!
class switch:
    def __init__(self, port, key1, key2): #This will setup our desired Button and bind it to uC!
        self.switch = digitalio.DigitalInOut(port) #Make a psychical Anchorn a INPUT!
        self.switch.switch_to_input(pull=digitalio.Pull.UP) #Make it HIGH!
        self.key1 = key1
        self.key2 = key2
        self.state = True #This will prevent us from unnecesary repeting
    def test_switch(self): #This will be testing state of Switch
        if self.switch.value != self.state:
            if self.switch.value == False: #This will execute if switch is ON!
                keyboard.press(self.key1)
                keyboard.release_all()
                time.sleep(400/1000)
                self.state = False
            else: #This will execute if switch is OFF!
                keyboard.press(self.key2)
                keyboard.release_all()
                time.sleep(400/1000)
                self.state = True

#Start of preparing THE RITUAL!

#Preparing a virtual keyboard, device used to comunicate with THE THING!
time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

#Preparing a psihical switch, a anchorn in real world!
s0 = switch(board.GP0,Keycode.ZERO,Keycode.C)
s1 = switch(board.GP1,Keycode.ONE,Keycode.C)
s2 = switch(board.GP2,Keycode.TWO,Keycode.C)
s3 = switch(board.GP3,Keycode.THREE,Keycode.C)
s4 = switch(board.GP4,Keycode.FOUR,Keycode.C)
s5 = switch(board.GP5,Keycode.FIVE,Keycode.C)
s6 = switch(board.GP6,Keycode.SIX,Keycode.C)


#Finally starting THE RITUAL!

print("hi")
while True:
    s0.test_switch()
    s1.test_switch()
    s2.test_switch()
    s3.test_switch()
    s4.test_switch()
    s5.test_switch()
    s6.test_switch()

