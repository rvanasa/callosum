#include "FastLED.h"

#define LED_PIN 5
#define NUM_LEDS 150
#define COLOR_ORDER GRB
//#define BRIGHTNESS 64
#define BRIGHTNESS 32
#define CONFIRMATION_LENGTH 8

CRGB leds[NUM_LEDS];
CRGB currentLeds[NUM_LEDS];

byte confirmations; // Confirmations before starting to read LED array

void setup() {
  Serial.begin(57600);

  FastLED.addLeds<WS2812B, LED_PIN, COLOR_ORDER>(currentLeds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  // Reset LED colors
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = 0;
    currentLeds[i] = 0;
  }
  FastLED.show();
}

void loop() {
//  leds[0] = CRGB::Red;
//  FastLED.show();
//  delay(1000);
  // leds[0] = 0x2255FF;
  // FastLED.show();
  // delay(1000);

//  Serial.println("Test");
//  Serial.flush();

//  delay(100);/////
  
  while(Serial.available() > 0) {
    byte signal = Serial.read();
    if(signal == 'A' + confirmations) {
      confirmations++;
      if(confirmations == CONFIRMATION_LENGTH) {
        confirmations = 0;

        while(Serial.available() < 3);
        float r = Serial.read() / 255.;
        float g = Serial.read() / 255.;
        float b = Serial.read() / 255.;
        
        for(int i = 0; i < NUM_LEDS; i++) {
//          while(Serial.available() < 3);
//          leds[i] = CRGB {.r = (byte)(Serial.read() * r), .g = (byte)(Serial.read() * g), .b = (byte)(Serial.read() * b)};

          while(Serial.available() < 1);
          byte a = Serial.read();
          leds[i] = CRGB {.r = (byte)(a * r), .g = (byte)(a * g), .b = (byte)(a * b)};
        }
      }
    }
    else {
      // Received unexpected byte
      confirmations = 0;
    }
  }

  for(int i = 0; i < NUM_LEDS; i++) {
//    currentLeds[i] = currentLeds[i].lerp8(leds[i], 16);
    currentLeds[i] = leds[i];
  }
  FastLED.show();
  delay(10);
}
