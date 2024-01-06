# xbox_msfs_autopilot
Autopilot DIY Project for MSFS on XBOX
## Credits to https://github.com/touchgadget/usb_keyboard_button_box_pico
## Features
The original code only supports one key at the same time.
Now you can define keycode, keycode2, keycode3 like:
{"pin":board.GP13, "keycode":Keycode.SHIFT, "keycode2":Keycode.U},

## PIN Layout for autopilot.py:

### Encoder

#### Bottom Encoder Heading Bug
GP0

GP1

GP2 Push

#### Top Encoder Altitude
GP3

GP4

GP5 Push

### Buttons

#### Top Right
GP6 ARM

GP7 Flight Director

#### Bottom Right
GP8 Vertical Speed DOWN

GP9 Verticaal Speed UP

#### Bottom 

GP10 ALT

GP11 APR

GP12 NAV

GP13 HDG

GP14 FLC

GP15 CDI

#### Top Left
GP16 AP

