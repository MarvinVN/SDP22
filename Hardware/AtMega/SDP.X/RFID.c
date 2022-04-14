/*
 * File:   RFID.c
 * Author: ray
 *
 * Created on February 8, 2022, 12:29 PM
 */
#define F_CPU 1000000UL
#include <xc.h>
#include "util/delay.h"
#include <stdlib.h>
#include <avr/io.h>
// ATmega328P Configuration Bit Settings
// 'C' source line config statements
void RotateReq(int req);
void dispensor(void);
void shuffler(void);
int position = 0;
FUSES = {
	.low = 0x7F, // LOW {SUT_CKSEL=EXTXOSC_8MHZ_XX_16KCK_14CK_65MS, CKOUT=CLEAR, CKDIV8=SET}
	.high = 0xD9, // HIGH {BOOTRST=CLEAR, BOOTSZ=2048W_3800, EESAVE=CLEAR, WDTON=CLEAR, SPIEN=SET, DWEN=CLEAR, RSTDISBL=CLEAR}
	.extended = 0xFF, // EXTENDED {BODLEVEL=DISABLED}
};

LOCKBITS = 0xFF; // {LB=NO_LOCK, BLB0=NO_LOCK, BLB1=NO_LOCK}


void main(void) {
    DDRC = 0xFF; // makes port C output
    DDRD &= ~(1 << PIND0);
    DDRD &= ~(1 << PIND1);
    DDRD &= ~(1 << PIND2);
    DDRC &= ~(1 << PINC5);
    DDRB = 0xFF; // makes port b output
    
    PORTB = 0b00000000;
    
    while(1){
        if(!(PIND&(1<<2)) && (!(PIND&(1<<1))) && ((PIND&(1<<0)))){
            RotateReq(0);
        }
        else if(!(PIND&(1<<2)) && ((PIND&(1<<1))) && (!(PIND&(1<<0)))){
            RotateReq(408);
        }
        else if(!(PIND&(1<<2)) && ((PIND&(1<<1))) && ((PIND&(1<<0)))){
            RotateReq(816);
        }
        else if((PIND&(1<<2)) && (!(PIND&(1<<1))) && (!(PIND&(1<<0)))){
            RotateReq(1224);
        }
        else if((PIND&(1<<2)) && (!(PIND&(1<<1))) && ((PIND&(1<<0)))){
            RotateReq(1632);
        }
        else if((PIND&(1<<2)) && ((PIND&(1<<1))) && ((PIND&(1<<0)))){
            shuffler();
        }
        else{
          _delay_ms(10);  
        }

    }
    return;
}


void shuffler(void){
    PORTB = 0b00000001;
    _delay_ms(5000);
    PORTB = 0b00000000;
}


void dispensor(void){
    PORTB = 0b00000010;
    _delay_ms(500);
    PORTB = 0b00000000;
}

void RotateReq(int req){
    _delay_ms(250);
    if (position > req){
        for(int i = 0; i<(position-req)/4; i++){
            PORTC = 0b00001001;
            _delay_ms(5);
            PORTC = 0b00001000;
            _delay_ms(5);
             PORTC = 0b00001100;
            _delay_ms(5);
            PORTC = 0b00000100;
            _delay_ms(5);
             PORTC = 0b000000110;
            _delay_ms(5);
            PORTC = 0b00000010;
            _delay_ms(5);
             PORTC = 0b00000011;
            _delay_ms(5);
            PORTC = 0b00000001;
            _delay_ms(5);
        }
    }else if (position < req){
        for(int i = 0; i<(req - position)/4; i++){
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
    }
    position = req;
    _delay_ms(500);
    dispensor();
    while(!(PINC&(1<<5))){
        if ((PIND&(1<<0))){
            dispensor(); 
        }
        _delay_ms(2000);
    }
    _delay_ms(500);
    PORTC = 0x09;
}
