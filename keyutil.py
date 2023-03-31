#!/usr/bin/env python
import tkinter as tk

keys = [None] * 256
filename = 'new_keymap.py'
window = tk.Tk(className='Keymap Utility')

def keydown(event):
    if hasattr(event, 'keycode'):
        keys[event.keycode] = event
        msg = "Keypress:  0x{:02X}  {}  {}".format(
            event.keycode, event.keycode, event.keysym)
    else:
        msg = 'Key not registered'
    l2.config(text=msg)
    print(event)

window.wm_title("Keymap Utility")
window.bind("<KeyPress>", keydown)
window.geometry('400x300')

l1 = tk.Label(window, text='Press all keyboard keys...')
l2 = tk.Label(window, text="")
l3 = tk.Label(window, text="Writing to: {}".format(filename))
l1.place(relx=.5, rely=.25, anchor="center")
l2.place(relx=.5, rely=.5, anchor="center")
l3.place(relx=.5, rely=1, anchor="s")

window.mainloop()

with open(filename, 'w') as file:
    file.write('''from enum import IntEnum

codes = [\n''')

    for code, key in enumerate(keys):
        sym = key.keysym if key else ''
        file.write("    0x00,   # {:02X}  {}\n".format(code, sym))

    file.write(''']

class keys(IntEnum):
    Ctrl   = 0x00
    Shift  = 0x00
    Alt    = 0x00
    Logo   = 0x00
    Menu   = 0x00\n''')

file.close()
