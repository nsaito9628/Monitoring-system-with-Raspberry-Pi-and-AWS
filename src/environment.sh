#!/bin/bash

sudo apt update  
sudo apt -y upgrade  
sudo apt install -y postfix docker awscli
sudo apt install libatlas-base-dev libjasper-dev -y
sudo apt install ffmpeg  libcanberra-gtk3-module v4l-utils qv4l2 -y
pip3 install paho-mqtt boto3 --upgrade
sudo pip3 install awscli aws-sam-cli --upgrade
python3 -m pip install opencv-python==4.5.4.60
pip3 install numpy --upgrade

cd /usr/bin
sudo rm python
sudo ln -s python3 python
cd