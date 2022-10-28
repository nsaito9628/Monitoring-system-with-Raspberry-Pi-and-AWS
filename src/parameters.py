import os
import datetime
import paho.mqtt.client as mqtt

#####################################################################
#environment for dashboard system
#####################################################################
HOST = os.environ['HOST_ENDPOINT']  # AWS IoT Endpoint
PORT = 8883  # mqtts port
CACERT = os.environ['CACERT']  # root ca
CLIENTCERT = os.environ['CLIENTCERT']  # certificate
CLIENTKEY = os.environ['CLIENTKEY']  # private key
TOPIC_DETECT_COUNT = os.environ['TOPIC_DETECT']  # topic
ID = TOPIC_DETECT_COUNT.split("/")[0]
client = mqtt.Client(client_id=ID, protocol=mqtt.MQTTv311)

DETECT_PIN = 21

SENSOR_NO = int(os.environ['SENSOR_NO'])

#####################################################################
#environment for cam system
#####################################################################
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']
S3BUCKET = os.environ['S3BUCKET']
TRIGGER_SELECT = int(os.environ['TRIGGER_SELECT'])

#####################################################################
#Select S3 prefix as distination of image
#####################################################################
PREFIX_IN =  os.environ['PREFIX_IN'] 

#resolution
#####################################
# 0: 176×144
# 1: 320×240
# 2: 640×480
# 3: 800×600
# 4: 1280×960
#####################################
res = 2 #Default resolution setting 2
resos = ([176, 144, 135, 25, 0.7],
         [320, 240, 230, 20, 1.3], 
         [640, 480, 470, 15, 2], 
         [800, 600, 585, 10, 2.2], 
         [1280, 720, 680, 5, 3.5])#Resolution / recording rate / caption position / frame rate / font size

#image Threshold when setting differential motion detection as trigger
thd = 30 #Threshold for bit judgment on 256-gradation gray scale
ratio = 0.1 #Threshold for motion detection judgment (area ratio exceeding bit judgment threshold to resolution)

#Video tmp file recording interval
interval = datetime.timedelta(seconds=4) #Record for 4 seconds if the sensor does not detect during the last recording loop
end_interval = datetime.timedelta(seconds=14, microseconds=150000) #Record for 14 seconds if the sensor detects it during the last recording loop