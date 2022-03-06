/*
 * File:   RFID.c
 * Author: ray
 *
 * Created on February 8, 2022, 12:29 PM
 */
#define F CPU 1000000UL	

#include <xc.h>
#include "util/delay.h"
#include <stdio.h>
#include <stdlib.h>
#include <avr/io.h>

// ATmega328P Configuration Bit Settings
// 'C' source line config statements
#include <avr/io.h>

FUSES = {
	.low = 0x7F, // LOW {SUT_CKSEL=EXTXOSC_8MHZ_XX_16KCK_14CK_65MS, CKOUT=CLEAR, CKDIV8=SET}
	.high = 0xD9, // HIGH {BOOTRST=CLEAR, BOOTSZ=2048W_3800, EESAVE=CLEAR, WDTON=CLEAR, SPIEN=SET, DWEN=CLEAR, RSTDISBL=CLEAR}
	.extended = 0xFF, // EXTENDED {BODLEVEL=DISABLED}
};

LOCKBITS = 0xFF; // {LB=NO_LOCK, BLB0=NO_LOCK, BLB1=NO_LOCK}



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

    //one revolution is 2048/4
    //to each player that is 2048/20 =~ 102.4
    
    /* loop */
    PORTD = 0b00000000;
    for(int i = 0; i<2048/4; i++){
        PORTC = 0b00000001;
        _delay_ms(5);
         PORTC = 0b00000011;
        _delay_ms(5);
        PORTC = 0b00000010;
        _delay_ms(5);
         PORTC = 0b000000110;
        _delay_ms(5);
        PORTC = 0b00000100;
        _delay_ms(5);
         PORTC = 0b00001100;
        _delay_ms(5);
        PORTC = 0b00001000;
        _delay_ms(5);
         PORTC = 0b00001001;
        _delay_ms(5);
    }
    PORTC = 0x09;
    _delay_ms(1000);
    
    

    PORTD = 0b00000001;
    _delay_ms(4000);
    PORTD = 0b00000010;
    _delay_ms(4000);
    PORTD = 0b00000011;
    PORTD = 0b00000000;
    
    
}





