/*
 * File:   RFID.c
 * Author: ray
 *
 * Created on February 8, 2022, 12:29 PM
 */
#define F_CPU 1000000UL

#include <xc.h>
#include "util/delay.h"
#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>
//#include <Adafruit_PN532.h>



char playerRequest;
int playerRequestInt;
const int Shuffler = 2;


void main(void) {
    DDRD = 0xFF; // makes port d output
    DDRB = 0xFF;
    //PORTD |= 0b00000010;   // turns on port pd0
    //_delay_ms(5000);
    //PORTD = 0x00;
    //_delay_ms(5000);        



    /* loop */
    while (1) {
        PORTB = 0b00000111;
        _delay_ms(200);
        PORTB = 0b00000011;
        _delay_ms(200);
        PORTB = 0b00001011;
        _delay_ms(200);
        PORTB = 0b00001001;
        _delay_ms(200);
        PORTB = 0b00001101;
        _delay_ms(200);
        PORTB = 0b00001100;
        _delay_ms(200);
        PORTB = 0b00001110;
        _delay_ms(200);
        PORTB = 0b00000110;
        _delay_ms(200);
    }
    return;
}

