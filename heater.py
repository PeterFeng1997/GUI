'''

    ************************************************************************
    *   FILE NAME:      heater.py
    *   AUTHOR:         Dylan Vogel, Peter Feng
    *   PURPOSE:        This file contains functions for heater control using PWM.
    *
    *
    *   EXTERNAL REFERENCES:    RPi.GPIO, thmcouple
    *
    *
    *   NOTES:          The only function you'll likely need to change is the constants
    *                   in initial_heating_time based on the thermal mass you're trying to heat.
    *
    *                   You could base these on calculations which take into account your input
    *                   wattage, thermal volume, convection, etc., but I find that it's easier to run
    *                   a characterization test and adjust based on that.
    *
    *   REVISION HISTORY:
    *
    *                   2017-05-22: Created file. Wrote basic functions.
    *                   2017-05-23: Wrote initial_heating_time based on empirically
    *                               derived values for our setup.
    *

'''

import RPi.GPIO as GPIO
import thmcouple as thm
import heatingProcess
global PWM_PIN_1, PWM_PIN_2, freq

# GPIO, not board pins on the RPi
PWM_PIN_1 = 23      # Center
PWM_PIN_2 = 24      # Edge

# PWM frequency in Hz
freq = 500

def setup1():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN_1, GPIO.OUT)

    pwm_1 = GPIO.PWM(PWM_PIN_1, freq)

    # Start both PWM channels at 0% duty cycle.
    pwm_1.start(0)

    return pwm_1

def setup2():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN_2, GPIO.OUT)

    pwm_2 = GPIO.PWM(PWM_PIN_2, freq)

    # Start both PWM channels at 0% duty cycle.
    pwm_2.start(0)

    return pwm_2

def initial_heating_time(process):
    # Apply some math to figure out how long to heat for.

    temp1 = thm.read(process.thm1)
    temp2 = thm.read(process.thm2)
    avg = (temp1 + temp2) / 2.0

    heating_time = ((process.temp - avg) / 2.0) - 4

    return heating_time

def initial_heating_time_new(process):
    # Revised method to determine the initial heating time

    temp1 = thm.read(process.thm1)
    temp2 = thm.read(process.thm2)
    avg = (temp1 + temp2) / 2.0

    temp_diff = process.temp - avg
    heating_time = (process.heat_capacity * process.mass * temp_diff / process.watt) - 10

    return heating_time

def calc_kp(work_temp):

    kp = 0.2 * ((work_temp / 100.0) * (work_temp / 100.0))
    kp = clamp(kp, 0.2, 1)

    return kp

def update_temp(temp_avg, temp):
    # Simple weighting scheme to smooth out large variations.
    new_temp = ((temp_avg * 2.0) + temp) / 3.0
    return new_temp

def change_duty(process):
    process.pwm_1.ChangeDutyCycle(process.pwm_center)
    process.pwm_2.ChangeDutyCycle(process.pwm_edge)

def clamp(n, minn, maxn):
    return max(min(n, maxn), minn)

def close(pwm):
    pwm.stop()
