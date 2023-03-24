# CrashCart

Use a laptop as a monitor and keyboard for another computer. Takes the place of
a traditional "crash cart" used in data centers to diagnose issues with headless
systems.

**Current Status**
CrashCart was written in a hurry to scratch a personal itch. It has been tested
primarily on Linux, but should work on Windows out of the box and on macOS
without many tweaks. Contributions are welcome, but feature requests without
an implementation are not likely to be considered. This is, at tbe end of the
day, a project aimed at tinkerers, and so OS packing is discouraged.

## Hardware

CrashCart displays the video stream from a video capture device connected to the
computer to monitor. It also captures key strokes and forwards them using a
keyboard emulator. 

### Video capture

Video can be displayed from any capture hardware supported by the kernel. A wide
variety of devices are available, including inexpensive USB capture dongles.

### Keyboard emulator

Keystrokes captured from the local keyboard are sent over a serial connection
using a simple protocol. The serial bridge can then be connected to a
microcontroller capable of emulating a USB keyboard, such as the Arduino
Leonardo (or clone) with an ATmega32u4. A sample program and keymap is
included.

## Install

CrashCart requires:

  * Python 3.7+
  * OpenCV 4
  * OpenCV-Python
  * Numpy
  * PySerial

On Linux, Your user account will also need access to `uinput`. This can be done
by running as root or, on some systems, by adding your user to the `tty` and/or
`input` groups.

    $ sudo usermod -a -G input,tty $USER

CrashCart can be run directly from the project source using the `run.py` script.

    $ ./run.py

It can also be installed using Python Build/Install:

    $ python -m build --wheel --no-isolation
    $ sudo python -m installer dist/*.whl

Or packaged on Arch Linux using the included `PKGBUILD`:

    $ cd pkg
    $ makepkg -si

## Use

CrashCart will attempt to select the correct video stream and serial port
when starting. To select another video device or serial device/speed, click
the right-most toolbar button, "Display properties window", to open the
control panel.

The control panel window allows you to cycle between video and serial devices
as well as serial device speeds. You can also disable keyboard capture, adjust
aspect ratio, and enable display of key presses in the status bar.

### Key Queue

Some key combinations may be intercepted or acted on by the host operating
system. To work around this issue, CrashCart provides buttons in the control
panel to "queue" certain keys to be sent directly to the connected computer,
without affecting the host OS.

The queued keys can be sent manually by pressing the "arrow/send" key at the
end of the second button row. They will also be sent automatically after the
next physical key press.

For example, to send the Logo (Windows) key to the connected computer, press
the `LOGO` button in the control panel, then the `->` button. To send
Ctrl-Alt-Del, press the `CTRL` and `ALT` buttons in the control panel, then
press the `Delete` key on the keyboard.

## Serial protocol

CrashCart sends key press and release events over a serial connection using a
simple protocol. Each command is followed by a newline.

  * Press key: `P <scan code>`
  * Release key: `R <scan code>`
  * Press and release key: `K <scan code>`

The decimal scan codes are the raw codes used by the Arduino Keyboard library.
For example, to press then release the Escape key:

    P 35
    R 35

CrashCart provides a mapping for standard PC keyboard scan codes in
`keymap.py`. If key presses are sending incorrect characters, you may need to
customize the keymap.

Copyright and License

Copyright (c) 2023 Corey Hinshaw  
Copyright (c) 2016 BoppreH

CrashCart is released under the terms of the MIT license. See the included
`LICENSE` file for details.
