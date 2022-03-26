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
// ATmega328P Configuration Bit Settings
// 'C' source line config statements
void fulldeal(void);
void p1(void);
void p2(void);
void p3(void);
void p4(void);
void p5(void);
void dispensor(void);
void shuffler(void);
FUSES = {
	.low = 0x7F, // LOW {SUT_CKSEL=EXTXOSC_8MHZ_XX_16KCK_14CK_65MS, CKOUT=CLEAR, CKDIV8=SET}
	.high = 0xD9, // HIGH {BOOTRST=CLEAR, BOOTSZ=2048W_3800, EESAVE=CLEAR, WDTON=CLEAR, SPIEN=SET, DWEN=CLEAR, RSTDISBL=CLEAR}
	.extended = 0xFF, // EXTENDED {BODLEVEL=DISABLED}
};

LOCKBITS = 0xFF; // {LB=NO_LOCK, BLB0=NO_LOCK, BLB1=NO_LOCK}


void main(void) {
    DDRD &= ~(1 << PIND0);
    DDRD &= ~(1 << PIND1);
    DDRD &= ~(1 << PIND2);
    DDRB = 0xFF; // makes port b output
    DDRC = 0xFF; // makes port C output
    
    PORTB = 0b00000000;
    
    while(1){
        p2();
    }
    
    while(1){
        if(!(PIND&(1<<2)) && (!(PIND&(1<<1))) && (PIND&(1<<0))){
            shuffler();
        }
        if(!(PIND&(1<<2)) && ((PIND&(1<<1))) && (!(PIND&(1<<0)))){
            fulldeal();
        }
        if(!(PIND&(1<<2)) && ((PIND&(1<<1))) && (PIND&(1<<0))){
            p1();
        }
        if((PIND&(1<<2)) && (!(PIND&(1<<1))) && (!(PIND&(1<<0)))){
            p2();
        }
        if((PIND&(1<<2)) && (!(PIND&(1<<1))) && (PIND&(1<<0))){
            p3();
        }
        if((PIND&(1<<2)) && (!(PIND&(1<<1))) && (PIND&(1<<0))){
            p4();
        }
        if((PIND&(1<<2)) && ((PIND&(1<<1))) && (PIND&(1<<0))){
            p5();
        }
    }
    return;
}


void shuffler(void){
    PORTB = 0b00000001;
    _delay_ms(4000);
    PORTB = 0b00000000;
}


void dispensor(void){
    PORTB = 0b00000010;
    _delay_ms(1000);
    PORTB = 0b00000000;
}

void p1(void){
    _delay_ms(1000);
    dispensor();
    _delay_ms(1000);
}
void p2(void){
        for(int i = 0; i<408/4; i++){
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
        _delay_ms(500);
        dispensor();
        _delay_ms(500);
        for(int i = 0; i<408/4; i++){
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
    _delay_ms(500);
}
void p3(void){
        for(int i = 0; i<2048/10; i++){
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
        dispensor();
        _delay_ms(1000);
        for(int i = 0; i<2048/10; i++){
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
    PORTC = 0x09;
    _delay_ms(1000); 
}
void p4(void){
        for(int i = 0; i<1228/4; i++){
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
        dispensor();
        _delay_ms(1000);
        for(int i = 0; i<1228/4; i++){
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
    PORTC = 0x09;
    _delay_ms(1000);
}
void p5(void){
    for(int i = 0; i<1640/4; i++){
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
        dispensor();
        _delay_ms(1000);
        for(int i = 0; i<1640/4; i++){
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
    PORTC = 0x09;
    _delay_ms(1000);
}


void fulldeal(void){  
    //one revolution is 2048/4
    //to each player that is 2048/20 =~ 102.4
    
    /* loop */
    _delay_ms(1000);
    dispensor();
    _delay_ms(1000);
    for(int j = 0; j<4; j++){
        for(int i = 0; i<2048/20; i++){
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
        _delay_ms(1000);
        dispensor();
        _delay_ms(1000);
    }
    for(int i = 0; i<(2048/4 - 2048/20); i++){
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
        PORTC = 0x09;
}





