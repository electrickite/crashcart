#include "Keyboard.h"

#define KBD_BUFFSZ 200

char in_ascii;
char kbd_buff[KBD_BUFFSZ];
int kbd_idx = 0;
int crs_idx = 0;

void SerialAnsiEsc(const char* seq) {
  char buff[10];
  snprintf(buff, sizeof(buff), "[%s", seq);
  Serial1.write(27);
  Serial1.print(buff);
}

void SerialClearLine() {
  SerialAnsiEsc("1G");
  SerialAnsiEsc("0J");
}

int convert_code(int code) {
  if (code < 128) {
    code = code + 136;
  }
  return code;
}

void press_key(char* codestr) {
  String code = codestr;
  Serial1.print("Press: ");
  Serial1.println(code);
  Keyboard.press(convert_code(code.toInt()));
}

void release_key(char* codestr) {
  String code = codestr;
  Serial1.print("Release: ");
  Serial1.println(code);
  Keyboard.release(convert_code(code.toInt()));
}

void command_parse(char* str) {
  char* pch;

  if (!(pch = strtok(str," "))) return;
  switch (pch[0]) {
    case 'P':
      // Press keycode
      if ((pch = strtok(NULL,""))) {
        press_key(pch);
      }
      break;
    case 'R':
      if ((pch = strtok(NULL,""))) {
        release_key(pch);
      }
      break;
    case 'K':
      if ((pch = strtok(NULL,""))) {
        press_key(pch);
        delay(200);
        release_key(pch);
      }
      break;
    default:
      Serial1.println("Invalid command");
  }
}

void read_serial(char in_ascii) {
  if(in_ascii == 10 || in_ascii == 13) {
    // LF or CR
    Serial1.println("");
    kbd_buff[kbd_idx] = '\0';
    command_parse(kbd_buff);
    crs_idx = kbd_idx;
    kbd_idx = 0;
  } else if (in_ascii == 3 || in_ascii == 27) {
    SerialClearLine();
    crs_idx = kbd_idx;
    kbd_idx = 0;
  } else if (kbd_idx >= KBD_BUFFSZ-1) {
    read_serial('\n');
  } else if (in_ascii <= 26) {
  } else {
    Serial1.write(in_ascii);
    if (crs_idx>kbd_idx) crs_idx = kbd_idx;
    kbd_buff[crs_idx++] = in_ascii;
    if (kbd_idx<crs_idx) kbd_idx++;
  }
}

void setup() {
  Serial1.begin(57600);
  Keyboard.begin();
  delay(1000);
  Serial1.println("Keyboard Emulator started");
}

void loop() {
  if (Serial1.available() > 0) {
    in_ascii = Serial1.read();

    if (in_ascii<0 || in_ascii>127)
      // Ignore non-basic ascii characters
      return;

    read_serial(in_ascii);
  }
}
