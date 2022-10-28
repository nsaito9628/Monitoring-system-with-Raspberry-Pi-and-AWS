#!/usr/bin/python
# -*- coding: utf-8 -*-import time
import datetime
import parameters as para


class Count:
    def __init__(self):
        return

    #If the sensor has HI output, increment the counter
    def motion_count(self, sig, motion_count):
            
        if sig == 1:
            motion_count = motion_count + 1
            print(motion_count)

        return motion_count