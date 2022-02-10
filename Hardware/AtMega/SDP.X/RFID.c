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
    DDRB = 0xFF;
    period = 100;	
    
    
    //PORTD |= 0b00000010;   // turns on port pd0
    //_delay_ms(5000);
    //PORTD = 0x00;
    //_delay_ms(5000);        



    /* loop */
    while(1){
        PORTB = 0x09;
        _delay_ms(1000);
        PORTB = 0x08;
        _delay_ms(1000);
        PORTB = 0x0C;
        _delay_ms(1000);
        PORTB = 0x04;
        _delay_ms(1000);
        PORTB = 0x06;
        _delay_ms(1000);
        PORTB = 0x02;
        _delay_ms(1000);
        PORTB = 0x03;
        _delay_ms(1000);
        PORTB = 0x01;
        _delay_ms(1000);
    }
    PORTB = 0x09;
    _delay_ms(1000);
}

