from enum import IntEnum

codes = [
    0x00,   # 00  
    0x00,   # 01  
    0x00,   # 02  
    0x00,   # 03  
    0x00,   # 04  
    0x00,   # 05  
    0x00,   # 06  
    0x00,   # 07  
    0xB2,   # 08  BackSpace
    0xB3,   # 09  Tab
    0x00,   # 0A  
    0x00,   # 0B  
    0x00,   # 0C  
    0xB0,   # 0D  Return
    0x00,   # 0E  
    0x00,   # 0F  
    0x85,   # 10  Shift
    0x84,   # 11  Control
    0x86,   # 12  Alt
    0xD0,   # 13  Pause
    0xC1,   # 14  Caps_Lock
    0x00,   # 15  
    0x00,   # 16  
    0x00,   # 17  
    0x00,   # 18  
    0x00,   # 19  
    0x00,   # 1A  
    0xB1,   # 1B  Escape
    0x00,   # 1C  
    0x00,   # 1D  
    0x00,   # 1E  
    0x00,   # 1F  
    0x2C,   # 20  space
    0xD3,   # 21  Prior
    0xD6,   # 22  Next
    0xD5,   # 23  End
    0xD2,   # 24  Home
    0xD8,   # 25  Left
    0xDA,   # 26  Up
    0xD7,   # 27  Right
    0xD9,   # 28  Down
    0x00,   # 29  
    0x00,   # 2A  
    0x00,   # 2B  
    0x00,   # 2C  
    0xD1,   # 2D  Insert
    0xD4,   # 2E  Delete
    0x00,   # 2F  
    0x27,   # 30  0
    0x1E,   # 31  1
    0x1F,   # 32  2
    0x20,   # 33  3
    0x21,   # 34  4
    0x22,   # 35  5
    0x23,   # 36  6
    0x24,   # 37  7
    0x25,   # 38  8
    0x26,   # 39  9
    0x00,   # 3A  
    0x00,   # 3B  
    0x00,   # 3C  
    0x00,   # 3D  
    0x00,   # 3E  
    0x00,   # 3F  
    0x00,   # 40  
    0x04,   # 41  a
    0x05,   # 42  b
    0x06,   # 43  c
    0x07,   # 44  d
    0x08,   # 45  e
    0x09,   # 46  f
    0x0A,   # 47  g
    0x0B,   # 48  h
    0x0C,   # 49  i
    0x0D,   # 4A  j
    0x0E,   # 4B  k
    0x0F,   # 4C  l
    0x10,   # 4D  m
    0x11,   # 4E  n
    0x12,   # 4F  o
    0x13,   # 50  p
    0x14,   # 51  q
    0x15,   # 52  r
    0x16,   # 53  s
    0x17,   # 54  t
    0x18,   # 55  u
    0x19,   # 56  v
    0x1A,   # 57  w
    0x1B,   # 58  x
    0x1C,   # 59  y
    0x1D,   # 5A  z
    0x83,   # 5B  Logo
    0x00,   # 5C  
    0xED,   # 5D  Menu
    0x00,   # 5E  
    0x00,   # 5F  
    0xEA,   # 60  KP0
    0xE1,   # 61  KP1
    0xE2,   # 62  KP2
    0xE3,   # 63  KP3
    0xE4,   # 64  KP4
    0xE5,   # 65  KP5
    0xE6,   # 66  KP6
    0xE7,   # 67  KP7
    0xE8,   # 68  KP8
    0xE9,   # 69  KP9
    0xDD,   # 6A  KP*
    0xDF,   # 6B  KP+
    0x00,   # 6C  
    0xDE,   # 6D  KP-
    0xEB,   # 6E  KP.
    0xDC,   # 6F  KP/
    0xC2,   # 70  F1
    0xC3,   # 71  F2
    0xC4,   # 72  F3
    0xC5,   # 73  F4
    0xC6,   # 74  F5
    0xC7,   # 75  F6
    0xC8,   # 76  F7
    0xC9,   # 77  F8
    0xCA,   # 78  F9
    0xCB,   # 79  F10
    0xCC,   # 7A  F11
    0xCD,   # 7B  F12
    0x00,   # 7C  
    0x00,   # 7D  
    0x00,   # 7E  
    0x00,   # 7F  
    0x00,   # 80  
    0x00,   # 81  
    0x00,   # 82  
    0x00,   # 83  
    0x00,   # 84  
    0x00,   # 85  
    0x00,   # 86  
    0x00,   # 87  
    0x00,   # 88  
    0x00,   # 89  
    0x00,   # 8A  
    0x00,   # 8B  
    0x00,   # 8C  
    0x00,   # 8D  
    0x00,   # 8E  
    0x00,   # 8F  
    0xDB,   # 90  Num_LocK
    0xCF,   # 91  Scroll_Lock
    0x00,   # 92  
    0x00,   # 93  
    0x00,   # 94  
    0x00,   # 95  
    0x00,   # 96  
    0x00,   # 97  
    0x00,   # 98  
    0x00,   # 99  
    0x00,   # 9A  
    0x00,   # 9B  
    0x00,   # 9C  
    0x00,   # 9D  
    0x00,   # 9E  
    0x00,   # 9F  
    0x00,   # A0  
    0x00,   # A1  
    0x00,   # A2  
    0x00,   # A3  
    0x00,   # A4  
    0x00,   # A5  
    0x00,   # A6  
    0x00,   # A7  
    0x00,   # A8  
    0x00,   # A9  
    0x00,   # AA  
    0x00,   # AB  
    0x00,   # AC  
    0x00,   # AD  
    0x00,   # AE  
    0x00,   # AF  
    0x00,   # B0  
    0x00,   # B1  
    0x00,   # B2  
    0x00,   # B3  
    0x00,   # B4  
    0x00,   # B5  
    0x00,   # B6  
    0x00,   # B7  
    0x00,   # B8  
    0x00,   # B9  
    0x33,   # BA  semicolon
    0x2E,   # BB  equal
    0x36,   # BC  comma
    0x2D,   # BD  minus
    0x37,   # BE  period
    0x38,   # BF  slash
    0x35,   # C0  grave
    0x00,   # C1  
    0x00,   # C2  
    0x00,   # C3  
    0x00,   # C4  
    0x00,   # C5  
    0x00,   # C6  
    0x00,   # C7  
    0x00,   # C8  
    0x00,   # C9  
    0x00,   # CA  
    0x00,   # CB  
    0x00,   # CC  
    0x00,   # CD  
    0x00,   # CE  
    0x00,   # CF  
    0x00,   # D0  
    0x00,   # D1  
    0x00,   # D2  
    0x00,   # D3  
    0x00,   # D4  
    0x00,   # D5  
    0x00,   # D6  
    0x00,   # D7  
    0x00,   # D8  
    0x00,   # D9  
    0x00,   # DA  
    0x2F,   # DB  bracketleft
    0x31,   # DC  backslash
    0x30,   # DD  bracketright
    0x34,   # DE  apostrophe
    0x00,   # DF  
    0x00,   # E0  
    0x00,   # E1  
    0x00,   # E2  
    0x00,   # E3  
    0x00,   # E4  
    0x00,   # E5  
    0x00,   # E6  
    0x00,   # E7  
    0x00,   # E8  
    0x00,   # E9  
    0x00,   # EA  
    0x00,   # EB  
    0x00,   # EC  
    0x00,   # ED  
    0x00,   # EE  
    0x00,   # EF  
    0x00,   # F0  
    0x00,   # F1  
    0x00,   # F2  
    0x00,   # F3  
    0x00,   # F4  
    0x00,   # F5  
    0x00,   # F6  
    0x00,   # F7  
    0x00,   # F8  
    0x00,   # F9  
    0x00,   # FA  
    0x00,   # FB  
    0x00,   # FC  
    0x00,   # FD  
    0x00,   # FE  
    0x00,   # FF  
]

class keys(IntEnum):
    Ctrl   = 0x11
    Shift  = 0x10
    Alt    = 0x12
    Logo   = 0x5B
    Menu   = 0x5D
