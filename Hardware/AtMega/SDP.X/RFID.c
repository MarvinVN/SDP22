/*
 * File:   RFID.c
 * Author: ray
 *
 * Created on February 8, 2022, 12:29 PM
 */


#include <xc.h>
#include "util/delay.h"
#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>
//#include <Adafruit_PN532.h>

#define PN532_SCK  (13)
#define PN532_MOSI (11)
#define PN532_SS   (10)
#define PN532_MISO (12)

char playerRequest;
int playerRequestInt;
const int Shuffler = 2;
//Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);


void main(void) {
    DDRD = 0xFF; // makes port d output
    while(1){
        PORTD |= 0b00000010;   // turns on port pd0
        _delay_ms(5000);
        PORTD = 0x00;
        _delay_ms(5000);        
    }

    return;
}
