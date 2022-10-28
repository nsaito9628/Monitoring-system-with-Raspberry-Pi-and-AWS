#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import parameters as para


class Sensor:
    def __init__(self):
        self.detect_pin = para.DETECT_PIN #Motion sensor signal port : GPIO 21
        self.sensor_no = para.SENSOR_NO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.detect_pin, GPIO.IN)
       

    #Output sensor HI / LO at 1/0
    def detect_counter(self): 
        sig = 0
        if self.sensor_no == 1:
            if GPIO.input(self.detect_pin) == GPIO.HIGH:
                sig = 0
            else:
                sig = 1
        else:
            if GPIO.input(self.detect_pin) == GPIO.HIGH:
                sig = 1

        return sig
