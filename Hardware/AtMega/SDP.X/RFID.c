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
#define IN1 PB1
#define IN2 PB2
#define IN3 PB3
#define IN4 PB4

#define SET(pin) (PORTB |= _BV(pin))
#define CLR(pin) (PORTB &= ~_BV(pin))

static int8_t _dir = 1;
static int8_t _seq = 0;

char playerRequest;
int playerRequestInt;
const int Shuffler = 2;

static void stepper_init(void)
{

    /* set step motor pins as OUTPUT */
    DDRB |= _BV(IN1)|_BV(IN2)|_BV(IN3)|_BV(IN4);
}

static void stepper_dir(uint8_t dir)
{
    _dir = !!(dir);
}

static void stepper_move(void)
{

    _seq = (_seq + (_dir?1:-1)) & 7;

    switch (_seq) {
    /* Pattern for 8 microsteps: A-AB-B-BC-C-CD-D-DA */
    /*      [   A   ][   B  ][   C   ][   D   ] */
    case 0: SET(IN1);CLR(IN2);CLR(IN3);CLR(IN4);break;
    case 1: SET(IN1);SET(IN2);CLR(IN3);CLR(IN4);break;
    case 2: CLR(IN1);SET(IN2);CLR(IN3);CLR(IN4);break;
    case 3: CLR(IN1);SET(IN2);SET(IN3);CLR(IN4);break;
    case 4: CLR(IN1);CLR(IN2);SET(IN3);CLR(IN4);break;
    case 5: CLR(IN1);CLR(IN2);SET(IN3);SET(IN4);break;
    case 6: CLR(IN1);CLR(IN2);CLR(IN3);SET(IN4);break;
    case 7: SET(IN1);CLR(IN2);CLR(IN3);SET(IN4);break;
    }

    _delay_ms(1); // 100Hz
}


void main(void) {
    DDRD = 0xFF; // makes port d output

    PORTD |= 0b00000010;   // turns on port pd0
    _delay_ms(5000);
    PORTD = 0x00;
    _delay_ms(5000);        

    uint8_t dir = 1;
    uint16_t step = 0;

    /* setup */
    stepper_init();

    /* loop */
    while (1) {
        stepper_dir(dir ^= 1);
        for (step = 0; step < 4096; ++step) {
            stepper_move(); // 1 step (1/4096)
        }
    }
    return;
}

