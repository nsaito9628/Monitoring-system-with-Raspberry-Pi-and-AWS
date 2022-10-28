#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import sys
from awsMQTTconnect import Com, Pub
from sensing import Sensor
from counter import Count


sensor = Sensor()
com = Com()
pub = Pub()
count = Count()

def loop():
    sub_t_count = 0
    detect_count = 0

    while True:
        sig_detect = sensor.detect_counter()
        detect_count = count.motion_count(sig_detect, detect_count)
        bool, sub_t_count = pub.publish_motion_count(sub_t_count, detect_count)
        #print(enter_count)
        if bool == True: 
            detect_count = 0
        
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        time.sleep(90)

        #wifi connection confirmation and MQTT connection
        com.get_ssid()
        com.aws_connect()

        #Main loop execution
        loop()

    except KeyboardInterrupt:
        sys.exit()
