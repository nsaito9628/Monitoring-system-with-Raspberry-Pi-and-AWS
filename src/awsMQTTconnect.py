#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import ssl
import time
from datetime import datetime 
import subprocess
import parameters as para



class Com:
    def __init__(self):
        self.client = para.client
        self.cacert = para.CACERT
        self.clientCert = para.CLIENTCERT
        self.clientKey = para.CLIENTKEY
        self.host = para.HOST
        self.port = para.PORT
    

    #Callback function when mqtt connection is successful
    def on_connect(self, client, userdata, flags, respons_code):
        #If the connection cannot be established, reboot after 90 seconds of waiting time for terminal access
        if respons_code != 0:
            print("respons_code:", respons_code, " flags:", flags)
            time.sleep(90)
            subprocess.call(["sudo","reboot"])
        print('Connected')


    #Function to determine the establishment of wifi connection
    def get_ssid(self):
        cmd = 'iwconfig wlan0|grep ESSID'
        r = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)\
            .stdout.decode().rstrip()
        idx = r.find('ESSID:')
        #If the connection cannot be established, reboot after 90 seconds of waiting time for terminal access
        if r[idx + 7:-1] == "ff/an":
            print("ESSID:", r[idx + 7:-1])
            time.sleep(90)
            subprocess.call(["sudo","reboot"])


    #Function that launches an MQTT client and creates an object instance
    def aws_connect(self):
        try:
            # certifications
            self.client.tls_set(
                self.cacert,
                certfile=self.clientCert,
                keyfile=self.clientKey,
                tls_version=ssl.PROTOCOL_TLSv1_2)
            self.client.tls_insecure_set(True)

            # callback
            self.client.on_connect = self.on_connect
            #client.on_disconnect = on_disconnect

            # port, keepalive
            self.client.connect(self.host, self.port, keepalive=60)

            self.client.loop_start()

        except KeyboardInterrupt:
            time.sleep(90)
            subprocess.call(["sudo","reboot"])


class Pub:
    def __init__(self):
        self.client = para.client
        self.topic_count = para.TOPIC_DETECT_COUNT


    #Function that dispenses motion sensor data to the cloud at 0 seconds per minute
    def publish_motion_count(self, sub_t_count, detect_count): 

        count_data = {} #KeyValue to publish
        t = datetime.now() 
        sub_t = str(t.minute/10)

        if sub_t[-1] != "0": 
            sub_t_count = 0

        if (sub_t[-1] == "0") and sub_t_count == 0:
            # IoTcoreへpublish
            count_data['Timestamp'] = int(time.time())
            count_data['detect_count'] = detect_count
            self.client.publish(self.topic_count, json.dumps(count_data, default=self.json_serial), qos=1) 
            print(count_data)

            sub_t_count = 1
            return True, sub_t_count
            
        if (t.minute == 0 or sub_t[-1] == 0) and sub_t_count == 1: 
            pass
            
        return False, sub_t_count


    def json_serial(self, para):
        return para.isoformat()
