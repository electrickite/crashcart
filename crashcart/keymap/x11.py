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
    0x00,   # 08  
    0xB1,   # 09  Escape
    0x1E,   # 0A  1
    0x1F,   # 0B  2
    0x20,   # 0C  3
    0x21,   # 0D  4
    0x22,   # 0E  5
    0x23,   # 0F  6
    0x24,   # 10  7
    0x25,   # 11  8
    0x26,   # 12  9
    0x27,   # 13  0
    0x2D,   # 14  minus
    0x2E,   # 15  equal
    0xB2,   # 16  BackSpace
    0xB3,   # 17  Tab
    0x14,   # 18  q
    0x1A,   # 19  w
    0x08,   # 1A  e
    0x15,   # 1B  r
    0x17,   # 1C  t
    0x1C,   # 1D  y
    0x18,   # 1E  u
    0x0C,   # 1F  i
    0x12,   # 20  o
    0x13,   # 21  p
    0x2F,   # 22  bracketleft
    0x30,   # 23  bracketright
    0xB0,   # 24  Return
    0x80,   # 25  Control_L
    0x04,   # 26  A
    0x16,   # 27  S
    0x07,   # 28  D
    0x09,   # 29  F
    0x0A,   # 2A  G
    0x0B,   # 2B  H
    0x0D,   # 2C  J
    0x0E,   # 2D  K
    0x0F,   # 2E  L
    0x33,   # 2F  semicolon
    0x34,   # 30  apostrophe
    0x35,   # 31  grave
    0x81,   # 32  Shift_L
    0x31,   # 33  backslash
    0x1D,   # 34  Z
    0x1B,   # 35  X
    0x06,   # 36  C
    0x19,   # 37  V
    0x05,   # 38  B
    0x11,   # 39  N
    0x10,   # 3A  M
    0x36,   # 3B  comma
    0x37,   # 3C  period
    0x38,   # 3D  slash
    0x85,   # 3E  Shift_R
    0xDD,   # 3F  KP_Multiply
    0x82,   # 40  Alt_L
    0x2C,   # 41  space
    0xC1,   # 42  Caps_Lock
    0xC2,   # 43  F1
    0xC3,   # 44  F2
    0xC4,   # 45  F3
    0xC5,   # 46  F4
    0xC6,   # 47  F5
    0xC7,   # 48  F6
    0xC8,   # 49  F7
    0xC9,   # 4A  F8
    0xCA,   # 4B  F9
    0xCB,   # 4C  F10
    0xDB,   # 4D  Num_Lock
    0xCF,   # 4E  Scroll_Lock
    0xE7,   # 4F  KP_7
    0xE8,   # 50  KP_8
    0xE9,   # 51  KP_9
    0xDE,   # 52  KP_Subtract
    0xE4,   # 53  KP_4
    0xE5,   # 54  KP_5
    0xE6,   # 55  KP_6
    0xDF,   # 56  KP_Add
    0xE1,   # 57  KP_1
    0xE2,   # 58  KP_2
    0xE3,   # 59  KP_3
    0xEA,   # 5A  KP_0
    0xEB,   # 5B  KP_Decimal
    0xCE,   # 5C  Print
    0x00,   # 5D  
    0x00,   # 5E  
    0xCC,   # 5F  F11
    0xCD,   # 60  F12
    0x00,   # 61  
    0x00,   # 62  
    0x00,   # 63  
    0x00,   # 64  
    0x00,   # 65  
    0x00,   # 66  
    0x00,   # 67  
    0xE0,   # 68  KP_Enter
    0x84,   # 69  Control_R
    0xDC,   # 6A  KP_Divide
    0x00,   # 6B  
    0x86,   # 6C  Alt_R
    0x00,   # 6D  
    0xD2,   # 6E  Home
    0xDA,   # 6F  Up
    0xD3,   # 70  Prior
    0xD8,   # 71  Left
    0xD7,   # 72  Right
    0xD5,   # 73  End
    0xD9,   # 74  Down
    0xD6,   # 75  Next
    0xD1,   # 76  Insert
    0xD4,   # 77  Delete
    0x00,   # 78  
    0x00,   # 79  
    0x00,   # 7A  
    0x00,   # 7B  
    0x00,   # 7C  
    0x00,   # 7D  
    0x00,   # 7E  
    0xD0,   # 7F  Pause
    0x00,   # 80  
    0x00,   # 81  
    0x00,   # 82  
    0x00,   # 83  
    0x00,   # 84  
    0x83,   # 85  Logo
    0x00,   # 86  
    0xED,   # 87  Menu
    0x00,   # 88  
    0x00,   # 89  
    0x00,   # 8A  
    0x00,   # 8B  
    0x00,   # 8C  
    0x00,   # 8D  
    0x00,   # 8E  
    0x00,   # 8F  
    0x00,   # 90  
    0x00,   # 91  
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
    0x00,   # BA  
    0x00,   # BB  
    0x00,   # BC  
    0x00,   # BD  
    0x00,   # BE  
    0x00,   # BF  
    0x00,   # C0  
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
    0x00,   # DB  
    0x00,   # DC  
    0x00,   # DD  
    0x00,   # DE  
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
    Ctrl   = 0x25
    Shift  = 0x32
    Alt    = 0x40
    Logo   = 0x85
    Menu   = 0x87
