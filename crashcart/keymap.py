from enum import IntEnum

codes = [
    0x00,   # 00
    0xB1,   # 01  ESC
    0x1E,   # 02  1!
    0x1F,   # 03  2@
    0x20,   # 04  3#
    0x21,   # 05  4$
    0x22,   # 06  5%
    0x23,   # 07  6^
    0x24,   # 08  77
    0x25,   # 09  8*
    0x26,   # 0A  9(
    0x27,   # 0B  0)
    0x2D,   # 0C  -_
    0x2E,   # 0D  =+
    0xB2,   # 0E  BACKSP
    0xB3,   # 0F  TAB
    0x14,   # 10  Q
    0x1A,   # 11  W
    0x08,   # 12  E
    0x15,   # 13  R
    0x17,   # 14  T
    0x1C,   # 15  Y
    0x18,   # 16  U
    0x0C,   # 17  I
    0x12,   # 18  O
    0x13,   # 19  P
    0x2F,   # 1A  [{
    0x30,   # 1B  ]}
    0xB0,   # 1C  ENTER
    0x80,   # 1D  LCTRL
    0x04,   # 1E  A
    0x16,   # 1F  S
    0x07,   # 20  D
    0x09,   # 21  F
    0x0A,   # 22  G
    0x0B,   # 23  H
    0x0D,   # 24  J
    0x0E,   # 25  K
    0x0F,   # 26  L
    0x33,   # 27  ;:
    0x34,   # 28  '"
    0x35,   # 29  `~
    0x81,   # 2A  LSHIFT
    0x31,   # 2B  \|
    0x1D,   # 2C  Z
    0x1B,   # 2D  X
    0x06,   # 2E  C
    0x19,   # 2F  V
    0x05,   # 30  B
    0x11,   # 31  N
    0x10,   # 32  M
    0x36,   # 33  ,<
    0x37,   # 34  .>
    0x38,   # 35  /?
    0x85,   # 36  RSHIFT
    0xDD,   # 37  KP*
    0x82,   # 38  LALT
    0x2C,   # 39  SPACE
    0xC1,   # 3A  CAPS
    0xC2,   # 3B  F1
    0xC3,   # 3C  F2
    0xC4,   # 3D  F3
    0xC5,   # 3E  F4
    0xC6,   # 3F  F5
    0xC7,   # 40  F6
    0xC8,   # 41  F7
    0xC9,   # 42  F8
    0xCA,   # 43  F9
    0xCB,   # 44  F10
    0xDB,   # 45  NUM
    0xCF,   # 46  SCROLL
    0xE7,   # 47  KP7
    0xE8,   # 48  KP8
    0xE9,   # 49  KP9
    0xDE,   # 4A  KP-
    0xE4,   # 4B  KP4
    0xE5,   # 4C  KP5
    0xE6,   # 4D  KP6
    0xDF,   # 4E  KP+
    0xE1,   # 4F  KP1
    0xE2,   # 50  KP2
    0xE3,   # 51  KP3
    0xEA,   # 52  KP0
    0xEB,   # 53  KP.
    0xCE,   # 54  PRNT
    0x00,   # 55
    0x00,   # 56
    0xCC,   # 57  F11
    0xCD,   # 58  F12
    0x00,   # 59
    0x00,   # 5A
    0x00,   # 5B
    0x00,   # 5C
    0x00,   # 5D
    0x00,   # 5E
    0x00,   # 5F
    0xE0,   # 60  KPENTER
    0x84,   # 61  RCTRL
    0xDC,   # 62  KP/
    0x00,   # 63
    0x86,   # 64  RALT
    0x00,   # 65
    0xD2,   # 66  HOME
    0xDA,   # 67  UP
    0xD3,   # 68  PGUP
    0xD8,   # 69  LEFT
    0xD7,   # 6A  RIGHT
    0xD5,   # 6B  END
    0xD9,   # 6C  DOWN
    0xD6,   # 6D  PGDN
    0xD1,   # 6E  INS
    0xD4,   # 6F  DEL
    0x00,   # 70
    0x00,   # 71
    0x00,   # 72
    0x00,   # 73
    0x00,   # 74
    0x00,   # 75
    0x00,   # 76
    0xD0,   # 77  PAUSE
    0x00,   # 78
    0x00,   # 79
    0x00,   # 7A
    0x00,   # 7B
    0x00,   # 7C
    0x83,   # 7D  LOGO
    0x00,   # 7E
    0xED    # 7F  MENU
]

class keys(IntEnum):
    Ctrl   = 0x1D
    Shift  = 0x2A
    Alt    = 0x38
    Logo   = 0x7D
    Menu   = 0x7F
