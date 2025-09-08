#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const uint16_t screen_Address = 0x3C;
const byte screen_Width = 128;
const byte screen_Height = 32;

Adafruit_SSD1306 oled_Display(screen_Width, screen_Height, &Wire, -1);

const byte pin_Sda = 4, pin_Scl = 5;
const byte pin_ButtonA = 2, pin_ButtonB = 13, pin_ButtonC = 14;
const byte pin_Knob = A0;

const float adc_Resolution = 1024;
const uint8_t total_Layers = 5;
const uint8_t total_Buttons = 3;

const unsigned long debounce_Time = 175;
const unsigned long delay_Time = 250;

unsigned long previous_Time = 0;
unsigned long previous_PressA = 0;
unsigned long previous_PressB = 0;
unsigned long previous_PressC = 0;

void setup() {
  Serial.begin(115200);
  pinMode(pin_ButtonA, INPUT_PULLUP);
  pinMode(pin_ButtonB, INPUT_PULLUP);
  pinMode(pin_ButtonC, INPUT_PULLUP);
  pinMode(pin_Knob, INPUT);

  Wire.begin(pin_Sda, pin_Scl);
  if(!oled_Display.begin(SSD1306_SWITCHCAPVCC, screen_Address)){
    Serial.println("Failed to initialize oled display");
  } 
}

void loop() {
  unsigned long current_Time = millis();

  uint8_t ButtonA = !digitalRead(pin_ButtonA);
  uint8_t ButtonB = !digitalRead(pin_ButtonB);
  uint8_t ButtonC = !digitalRead(pin_ButtonC);
  uint16_t current_Knob   = analogRead(pin_Knob);
  uint8_t  current_Layer = ceil(total_Layers * (current_Knob / adc_Resolution)) - 1;
 
  if(current_Time - previous_Time >= delay_Time){
    Serial.println(current_Layer);
    oled_Display.clearDisplay();
    previous_Time = current_Time;
  }

  if(ButtonA){
    if(current_Time - previous_PressA > debounce_Time){
      previous_PressA = current_Time;
      uint8_t current_Button = 1 + total_Buttons * current_Layer;
      Serial.print("Button Pressed : "); Serial.println(current_Button);
      DrawCircle(0, 0, 1);
    }
  }
  if(ButtonB){
    if(current_Time - previous_PressB > debounce_Time){
      previous_PressB = current_Time;
      uint8_t current_Button = 2 + total_Buttons * current_Layer;
      Serial.print("Button Pressed : "); Serial.println(current_Button);
      DrawCircle(0, 1, 0);
    }
  }
  if(ButtonC){
    if(current_Time - previous_PressC > debounce_Time){
      previous_PressC = current_Time;
      uint8_t current_Button = 3 + total_Buttons * current_Layer;
      Serial.print("Button Pressed : "); Serial.println(current_Button);
      DrawCircle(1, 0, 0);
    }
  }

  String Text = "Layer -> " + String((current_Layer+1));
  WriteText(Text);
}

void WriteText(String Text){
  oled_Display.setTextSize(2);
  oled_Display.setTextColor(SSD1306_WHITE);
  oled_Display.setCursor(7, 0);
  oled_Display.println(Text);
  oled_Display.display();
}

void DrawCircle(bool Circle1, bool Circle2, bool Circle3){
  uint8_t y = 24;
  if(Circle1){
    oled_Display.drawCircle(32, y, 6, SSD1306_WHITE);
    oled_Display.drawCircle(32, y, 5, SSD1306_WHITE);
    oled_Display.drawCircle(32, y, 4, SSD1306_WHITE);
    oled_Display.drawCircle(32, y, 3, SSD1306_WHITE);
  }
  if(Circle2){
    oled_Display.drawCircle(64, y, 6, SSD1306_WHITE);
    oled_Display.drawCircle(64, y, 5, SSD1306_WHITE);
    oled_Display.drawCircle(64, y, 4, SSD1306_WHITE);
    oled_Display.drawCircle(64, y, 3, SSD1306_WHITE);
  }
  if(Circle3){
    oled_Display.drawCircle(96, y, 6, SSD1306_WHITE);
    oled_Display.drawCircle(96, y, 5, SSD1306_WHITE);
    oled_Display.drawCircle(96, y, 4, SSD1306_WHITE);
    oled_Display.drawCircle(96, y, 3, SSD1306_WHITE);
  }
  oled_Display.display();
}