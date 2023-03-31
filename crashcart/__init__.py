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

import cv2
import glob
import importlib.util
import numpy as np
import os
import serial
import sys
import threading
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from serial.tools.list_ports import comports as list_ports

try:
    from .keymap import custom as keymap
except ImportError:
    if importlib.util.find_spec('crashcart_keymap'):
        import crashcart_keymap as keymap
    elif sys.platform == 'linux':
        from .keymap import x11 as keymap
    elif sys.platform == 'win32':
        from .keymap import win as keymap
    else:
        from .keymap import linux as keymap


class App:

    def __init__(self):
        self.window = None
        self.window_resized = False
        self.video = None
        self.statusbar = None
        self.cp = None
        self.vc = None
        self.vc_index = 0
        self.aspect = None
        self.vid_width = None
        self.vid_height = None
        self.ser = None
        self.ser_index = 0
        self.ports = []
        self.keyboard_enabled = True
        self.show_keys = False
        self.last_key = None
        self.key_queue = []

        self.baud_index = 15
        self.baud_rates = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200];

        self.blank = np.zeros((480, 640, 3), np.uint8)
        self.blank[:] = (0, 0, 0)

    def show_control_panel(self, event=None):
        if self.cp and self.cp.winfo_exists(): return
        self.cp = tk.Toplevel()
        self.cp.wm_title("Control Panel")
        self.cp.resizable(width=False, height=False)
        self.cp.attributes('-topmost', 'true')
        self.cp.bind("<KeyPress>", self.keydown)
        self.cp.bind("<KeyRelease>", self.keyup)

        kbChk = tk.BooleanVar()
        kbChk.set(self.keyboard_enabled)
        showChk = tk.BooleanVar()
        showChk.set(self.show_keys)

        frame = tk.Frame(self.cp, borderwidth=0, relief="flat")
        frame.pack(padx=15, pady=10)
        frame.grid_columnconfigure(1, weight=1, uniform="a")
        frame.grid_columnconfigure(2, weight=1, uniform="a")
        sc = frame.cget('bg')

        tk.Label(frame, text="Key Queue").grid(
            row=0, column=0, columnspan=3, pady=(0,6))
        tk.Button(frame, text="CTRL", command=lambda:self.queue_key(keymap.keys.Ctrl)).grid(
            row=1, column=0, sticky='nesw', padx=2, pady=2)
        tk.Button(frame, text="SHFT", command=lambda:self.queue_key(keymap.keys.Shift)).grid(
            row=1, column=1, sticky='nesw', padx=2, pady=2)
        tk.Button(frame, text="ALT ", command=lambda:self.queue_key(keymap.keys.Alt)).grid(
            row=1, column=2, sticky='nesw', padx=2, pady=2)
        tk.Button(frame, text="LOGO", command=lambda:self.queue_key(keymap.keys.Logo)).grid(
            row=2, column=0, sticky='nesw', padx=2, pady=2)
        tk.Button(frame, text="MENU", command=lambda:self.queue_key(keymap.keys.Menu)).grid(
            row=2, column=1, sticky='nesw', padx=2, pady=2)
        tk.Button(frame, text=" -> ", command=lambda:self.send_keys(self.key_queue)).grid(
            row=2, column=2, sticky='nesw', padx=2, pady=2)
        tk.Label(frame, text="Settings").grid(
            row=3, column=0, columnspan=3, pady=(18,6))
        tk.Button(frame, text="<<", command=self.prev_stream).grid(
            row=4, column=0, sticky='nesw', pady=2)
        tk.Label(frame, text="Stream").grid(
            row=4, column=1, pady=2)
        tk.Button(frame, text=">>", command=self.next_stream).grid(
            row=4, column=2, sticky='nesw', pady=2)
        tk.Button(frame, text="<<", command=self.prev_serial).grid(
            row=5, column=0, sticky='nesw', pady=2)
        tk.Label(frame, text="Serial").grid(
            row=5, column=1, pady=2)
        tk.Button(frame, text=">>", command=self.next_serial).grid(
            row=5, column=2, sticky='nesw', pady=2)
        tk.Button(frame, text="<<", command=self.prev_baud).grid(
            row=6, column=0, sticky='nesw', pady=2)
        tk.Label(frame, text="Speed").grid(
            row=6, column=1, pady=2)
        tk.Button(frame, text=">>", command=self.next_baud).grid(
            row=6, column=2, sticky='nesw', pady=2)
        tk.Label(frame, text="Aspect Ratio").grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(12,0))
        tk.Radiobutton(frame, text="Orig", selectcolor=sc, borderwidth=0, highlightthickness=0, variable=self.aspect, value='native', command=lambda:self.set_aspect()).grid(
            row=8, column=0, sticky='w')
        tk.Radiobutton(frame, text="4:3", selectcolor=sc, borderwidth=0, highlightthickness=0, variable=self.aspect, value='std', command=lambda:self.set_aspect()).grid(
            row=8, column=1, sticky='w')
        tk.Radiobutton(frame, text="16:9", selectcolor=sc, borderwidth=0, highlightthickness=0, variable=self.aspect, value='wide', command=lambda:self.set_aspect()).grid(
            row=8, column=2, sticky='w')
        tk.Checkbutton(frame, text="Enable Keyboard", variable=kbChk, command=lambda:self.enable_keyboard(kbChk.get()), borderwidth=0, highlightthickness=0, selectcolor=sc).grid(
            row=9, column=0, columnspan=3, sticky='w', pady=(12,4))
        tk.Checkbutton(frame, text="Show Keys", variable=showChk, command=lambda:self.set_show_keys(showChk.get()), borderwidth=0, highlightthickness=0, selectcolor=sc).grid(
            row=10, column=0, columnspan=3, sticky='w', pady=4)

    def fit_image(self, img):
        win_width = self.window.winfo_width()
        win_height = self.window.winfo_height() - self.statusbar.winfo_reqheight()
        return ImageOps.contain(img, (win_width, win_height), method=Image.BICUBIC)

    def serial_write(self, msg):
        if self.ser:
            self.ser.write(bytes(msg, 'utf-8'))

    def print_key(self, key, action):
        if self.show_keys:
            print('{}  0x{:02X}  {:<3} {}'.format(
                action, key.keycode, key.keycode, key.keysym))

    def map_keycode(aelf, code):
        try:
            return keymap.codes[code]
        except IndexError:
            return 0x00

    def send_key_press(self, code):
        self.serial_write("P {}\n".format(self.map_keycode(code)))

    def send_key_release(self, code):
        self.serial_write("R {}\n".format(self.map_keycode(code)))

    def keydown(self, event):
        if not self.keyboard_enabled: return
        self.print_key(event, 'PRESS  ')
        if self.key_queue:
            self.send_keys(keys=self.key_queue)
        self.send_key_press(event.keycode)
        self.last_key = event

    def keyup(self, event):
        if not self.keyboard_enabled: return
        self.print_key(event, 'RELEASE')
        self.send_key_release(event.keycode)

    def start_serial(self):
        self.stop_serial()
        try:
            self.ser = serial.Serial(self.ports[self.ser_index].device, self.baud_rates[self.baud_index])
            print("Opened serial connection: {} {} {}{}{}".format(
                self.ser.name, self.ser.baudrate, self.ser.bytesize, self.ser.parity, self.ser.stopbits))
        except IndexError:
            print("Serial port not found", file=sys.stderr)
        except:
            print("Could not open serial connection: {}".format(self.ports[self.ser_index].name), file=sys.stderr)

    def stop_serial(self):
        if self.ser: self.ser.close()

    def start_capture(self):
        try:
            self.stop_capture()
            if sys.platform == 'linux':
                self.vc = cv2.VideoCapture(self.vc_index, cv2.CAP_V4L)
            elif sys.platform == 'win32':
                self.vc = cv2.VideoCapture(self.vc_index, cv2.CAP_DSHOW)
            elif sys.platform == 'darwin':
                self.vc = cv2.VideoCapture(self.vc_index, cv2.CAP_AVFOUNDATION)
            if not (self.vc and self.vc.isOpened()):
                self.vc = cv2.VideoCapture(self.vc_index, cv2.CAP_ANY)
            self.vc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            if self.vid_width:
                self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, self.vid_width)
                self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, self.vid_height)
            self.window_resized = False
        except:
            vc = None

    def stop_capture(self):
        if self.vc: self.vc.release()

    def status_str(self):
        stream = "{} x {}".format(
            int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))) if self.vc and self.vc.isOpened() else 'No Video'
        ser_info = "{} {} {}{}{}".format(
            self.ser.name, self.ser.baudrate, self.ser.bytesize, self.ser.parity, self.ser.stopbits) if self.ser else None
        kb = 'Enabled' if self.keyboard_enabled else 'Disabled'
        key = "  0x{:02X} {}".format(self.last_key.keycode, self.last_key.keysym) if self.show_keys and self.last_key else ''
        q = "  |  Q: {}".format(', '.join(list(map(lambda k : str(k).split('.')[-1], self.key_queue)))) if self.key_queue else ''
        return "Video: [{}] {}  |  Serial: {}  |  Keyboard: {}{}{}".format(
            self.vc_index, stream, ser_info, kb, key, q)

    def prev_stream(self):
        if self.vc_index == 0: return
        self.vc_index -= 1
        self.start_capture()

    def next_stream(self):
        self.vc_index += 1
        self.start_capture()

    def prev_serial(self):
        self.ser_index = len(self.ports)-1 if self.ser_index == 0 else self.ser_index-1
        self.start_serial()

    def next_serial(self):
        self.ser_index = 0 if self.ser_index == len(self.ports)-1 else self.ser_index+1
        self.start_serial()

    def prev_baud(self):
        self.baud_index = len(self.baud_rates)-1 if self.baud_index == 0 else self.baud_index-1
        self.start_serial()

    def next_baud(self):
        self.baud_index = 0 if self.baud_index == len(self.baud_rates)-1 else self.baud_index+1
        self.start_serial()

    def enable_keyboard(self, state=True):
        self.keyboard_enabled = bool(state)

    def set_show_keys(self, show=True):
        self.show_keys = bool(show)

    def set_aspect(self, mode=None):
        new_mode = mode if mode else self.aspect.get()
        if new_mode == 'std':
            self.vid_width = 1024
            self.vid_height = 768
        elif new_mode == 'wide':
            self.vid_width = 1280
            self.vid_height = 720
        else:
            self.vid_width = None
            self.vid_height = None
        self.start_capture()

    def queue_key(self, key):
        if key in self.key_queue:
            self.key_queue.remove(key)
        self.key_queue.append(key)

    def send_keys(self, keys=[], press=True):
        if press:
            for key in keys:
                self.send_key_press(key)
            timer = threading.Timer(0.25, self.send_keys, None, {'keys': keys[:], 'press': False})
            timer.start()
            keys.clear()
        else:
            for key in keys:
                self.send_key_release(key)

    def show_frame(self):
        try:
            if self.vc.isOpened():
                ret, frame = self.vc.read()
            else:
                ret = False
            if not ret:
                frame = self.blank
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            if self.window_resized:
                img = self.fit_image(img)
            else:
                imw, imh = img.size
                self.window.geometry("{}x{}".format(imw, imh))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video.imgtk = imgtk
            self.video.configure(image=imgtk)
            self.statusbar.configure(text=self.status_str())
            self.window_resized = True
        except:
            pass
        self.window.after(30, self.show_frame)

    def run(self):
        self.ports = list_ports()
        self.ports.sort(key=lambda p: p.name)
        for index, port in enumerate(self.ports):
            if 'USB' in port.name:
                self.ser_index = index
                break

        if len(glob.glob('/dev/video*')) > 2:
            self.vc_index = 2

        self.start_serial()
        self.start_capture()

        self.window = tk.Tk(className='CrashCart')
        self.window.wm_title('CrashCart')
        self.window.bind('<Control-Key-p>', self.show_control_panel)
        self.window.bind("<KeyPress>", self.keydown)
        self.window.bind("<KeyRelease>", self.keyup)
        self.window.bind("<Button-3>", self.show_control_panel)

        self.video = tk.Label(self.window, relief='flat', borderwidth=0)
        self.video.pack(anchor=tk.CENTER, expand=True)
        self.statusbar = tk.Label(self.window, text=self.status_str(), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.aspect = tk.StringVar(self.window, 'native')

        self.show_frame()
        self.window.mainloop()

        self.stop_capture()
        self.stop_serial()
        return 0


def run():
    app = App()
    return app.run()
