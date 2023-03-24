"""
Copyright (c) 2023 Corey Hinshaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from . import keyboard
from . import keymap
import cv2
import glob
import numpy as np
import os
import serial
import sys
import threading
from serial.tools.list_ports import comports as list_ports

window = 'main'
vc = None
vc_index = 0
ser = None
ser_index = 0
keyboard_enabled = True
show_keys = False
last_key = None
key_queue = []
vid_width = 1920
vid_height = 1080

baud_index = 15
baud_rates = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200];

ports = list_ports()
ports.sort(key=lambda p: p.name)
for index, port in enumerate(ports):
    if 'USB' in port.name:
        ser_index = index
        break

if len(glob.glob('/dev/video*')) > 2:
    vc_index = 2

blank = np.zeros((300, 400, 3), np.uint8)
blank[:] = (0, 0, 0)

def serial_write(msg):
    if ser:
        ser.write(bytes(msg, 'utf-8'))

def print_key(key, action):
    if show_keys:
        print('{}  0x{:02X}  {:<3} {}'.format(
            action, key.scan_code, key.scan_code, key.name))

def map_scancode(code):
    try:
        return keymap.codes[code]
    except IndexError:
        return 0x00

def send_key_press(code):
    serial_write("P {}\n".format(map_scancode(code)))

def send_key_release(code):
    serial_write("R {}\n".format(map_scancode(code)))

def key_hook(event):
    global last_key
    if not keyboard_enabled: return
    if event.event_type == keyboard.KEY_DOWN:
        print_key(event, 'PRESS  ')
        if key_queue:
            send_keys(keys=key_queue)
        send_key_press(event.scan_code)
        last_key = event
    if event.event_type == keyboard.KEY_UP:
        print_key(event, 'RELEASE')
        send_key_release(event.scan_code)

def start_serial():
    global ser
    stop_serial()
    try:
        ser = serial.Serial(ports[ser_index].device, baud_rates[baud_index])
        print("Opened serial connection: {} {} {}{}{}".format(
            ser.name, ser.baudrate, ser.bytesize, ser.parity, ser.stopbits))
    except IndexError:
        print("Serial port not found", file=sys.stderr)
    except:
        print("Could not open serial connection: {}".format(ports[ser_index].name), file=sys.stderr)

def stop_serial():
    if ser: ser.close()

def start_capture():
    global vc
    try:
        stop_capture()
        vc = cv2.VideoCapture(vc_index, cv2.CAP_V4L)
        if not vc.isOpened():
          vc = cv2.VideoCapture(vc_index, cv2.CAP_DSHOW)
        if not vc.isOpened():
          vc = cv2.VideoCapture(vc_index, cv2.CAP_ANY)
        vc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        vc.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
        vc.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
    except:
        vc = None

def stop_capture():
    if vc: vc.release()

def status_str():
    stream = "{} x {}".format(
        int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))) if vc and vc.isOpened() else 'None'
    ser_info = "{} {} {}{}{}".format(
        ser.name, ser.baudrate, ser.bytesize, ser.parity, ser.stopbits) if ser else None
    kb = 'Enabled' if keyboard_enabled else 'Disabled'
    key = "  0x{:02X} {}".format(last_key.scan_code, last_key.name) if show_keys and last_key else ''
    q = "  |  Q: {}".format(', '.join(list(map(lambda k : str(k).split('.')[-1], key_queue)))) if key_queue else ''
    return "Video: [{}] {}  |  Serial: {}  |  Keyboard: {}{}{}".format(
        vc_index, stream, ser_info, kb, key, q)

def toggle_stream(state=None, next=True):
    global vc_index
    if next:
        vc_index += 1
    else:
        if vc_index == 0: return
        vc_index -= 1
    start_capture()

def toggle_serial(state=None, next=True):
    global ser_index
    if next:
        ser_index = 0 if ser_index == len(ports)-1 else ser_index+1
    else:
        ser_index = len(ports)-1 if ser_index == 0 else ser_index-1
    start_serial()

def toggle_baud(state=None, next=True):
    global baud_index
    if next:
        baud_index = 0 if baud_index == len(baud_rates)-1 else baud_index+1
    else:
        baud_index = len(baud_rates)-1 if baud_index == 0 else baud_index-1
    start_serial()

def enable_keyboard(state, data):
    global keyboard_enabled
    keyboard_enabled = bool(state)

def aspect_ratio(state, data):
    global vid_width
    global vid_height
    if state:
        vid_width = 1920
        vid_height = 1080
    else:
        vid_width = 1024
        vid_height = 768
    start_capture()

def set_show_keys(state, data):
    global show_keys
    show_keys = bool(state)

def queue_key(state=None, data=None):
    global key_queue
    if data in key_queue:
        key_queue.remove(data)
    key_queue.append(data)

def send_keys(state=None, keys=[], press=True):
    if press:
        for key in keys:
            send_key_press(key)
        timer = threading.Timer(0.25, send_keys, None, {'keys': keys[:], 'press': False})
        timer.start()
        keys.clear()
    else:
        for key in keys:
            send_key_release(key)

def run():
    start_serial()
    keyboard.hook(key_hook)
    start_capture()

    cv2.namedWindow(window, cv2.WINDOW_GUI_EXPANDED|cv2.WINDOW_KEEPRATIO|cv2.WINDOW_NORMAL)
    cv2.setWindowTitle(window, 'CrashCart')
    cv2.resizeWindow(window, 800, 600)
    cv2.createButton('CTRL', queue_key, keymap.keys.Ctrl)
    cv2.createButton('SHFT', queue_key, keymap.keys.Shift)
    cv2.createButton('ALT ', queue_key, keymap.keys.Alt)
    cv2.createButton('LOGO', queue_key, keymap.keys.Logo, cv2.QT_PUSH_BUTTON|cv2.QT_NEW_BUTTONBAR)
    cv2.createButton('MENU', queue_key, keymap.keys.Menu)
    cv2.createButton(' -> ', send_keys, key_queue)
    cv2.createButton('< Stream', toggle_stream, False, cv2.QT_PUSH_BUTTON|cv2.QT_NEW_BUTTONBAR)
    cv2.createButton('Stream >', toggle_stream, True)
    cv2.createButton('< Serial', toggle_serial, False, cv2.QT_PUSH_BUTTON|cv2.QT_NEW_BUTTONBAR)
    cv2.createButton('Serial >', toggle_serial, True)
    cv2.createButton('- Speed', toggle_baud, False, cv2.QT_PUSH_BUTTON|cv2.QT_NEW_BUTTONBAR)
    cv2.createButton('Speed +', toggle_baud, True)
    cv2.createButton('Enable Keyboard', enable_keyboard, None, cv2.QT_CHECKBOX|cv2.QT_NEW_BUTTONBAR, 1)
    cv2.createButton('Widescreen', aspect_ratio, None, cv2.QT_CHECKBOX|cv2.QT_NEW_BUTTONBAR, 1)
    cv2.createButton('Show Keys', set_show_keys, None, cv2.QT_CHECKBOX|cv2.QT_NEW_BUTTONBAR, 0)

    while True:
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False
        if not rval:
            frame = blank
            cv2.displayOverlay(window, 'No Video', 35)
        cv2.displayStatusBar(window, status_str(), 0)
        cv2.imshow(window, frame)
        key = cv2.waitKey(30)
        if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    stop_capture()
    stop_serial()
