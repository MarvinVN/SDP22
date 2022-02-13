/*
 * File:   RFID.c
 * Author: ray
 *
 * Created on February 8, 2022, 12:29 PM
 */
#define F_CPU 8000000UL	

#include <xc.h>
#include "util/delay.h"
#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>
//#include <Adafruit_PN532.h>



char playerRequest;
int playerRequestInt;
const int Shuffler = 2;
int period;


void main(void) {
    DDRD = 0xFF; // makes port d output
    DDRC = 0x0F;
    period = 100;	
    
    
    //PORTD |= 0b00000010;   // turns on port pd0
    //_delay_ms(5000);
    //PORTD = 0x00;
    //_delay_ms(5000);        



    /* loop */
    while(1){
        PORTC = 0b00000001;
        _delay_ms(2);
         PORTC = 0b00000011;
        _delay_ms(2);
        PORTC = 0b00000010;
        _delay_ms(2);
         PORTC = 0b000000110;
        _delay_ms(2);
        PORTC = 0b00000100;
        _delay_ms(2);
         PORTC = 0b00001100;
        _delay_ms(2);
        PORTC = 0b00001000;
        _delay_ms(2);
         PORTC = 0b00001001;
        _delay_ms(2);


    }
    PORTC = 0x09;
    _delay_ms(1000);
}

