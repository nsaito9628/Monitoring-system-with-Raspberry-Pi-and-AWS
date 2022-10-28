#!/bin/bash

#/home/pi/ --> mkdir cert && cd cert && cp iot_prov.sh
sudo apt install jq -y
sudo apt update -y
sudo apt upgrade -y

#THING NAME (is same as Project Name)
THING_NAME=$(cat ./iot_prov_config | grep THING_NAME | awk -F'=' '{print $2}')

# create the thing
aws iot create-thing --thing-name ${THING_NAME} | tee create-thing.json
 
# create and download the keys and device certificate
aws iot create-keys-and-certificate --certificate-pem-outfile ${THING_NAME}-certificate.pem.crt --public-key-outfile ${THING_NAME}-public.pem.key --private-key-outfile ${THING_NAME}-private.pem.key --set-as-active | tee create-keys-and-certificate.json
 
# create the thing policy
aws iot create-policy --policy-name ${THING_NAME}_all_access --policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["iot:*"], "Resource": ["*"]}]}'
 
# attach the certificate to the thing
CERT_ARN=$(jq -r '.certificateArn' < create-keys-and-certificate.json)
aws iot attach-thing-principal --thing-name ${THING_NAME} --principal ${CERT_ARN}
 
# attach policy to the certificate
aws iot attach-policy --policy-name ${THING_NAME}_all_access --target ${CERT_ARN}
 
# download the amazon root ca
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem
 
# find out what endpoint we need to connect to
echo $(aws iot describe-endpoint --endpoint-type iot:Data-ATS --region ap-northeast-1) >> end_point.json

# creating cron_mod.conf
echo HOST_ENDPOINT=$(jq -r '.endpointAddress' < ./end_point.json) >> cron_mod.conf
echo CACERT=./cert/AmazonRootCA1.pem >> cron_mod.conf
echo CLIENTCERT=./cert/${THING_NAME}-certificate.pem.crt >> cron_mod.conf
echo CLIENTKEY=./cert/${THING_NAME}-private.pem.key >> cron_mod.conf
echo >> cron_mod.conf
echo TOPIC_DETECT="${THING_NAME}/count" >> cron_mod.conf
echo >> cron_mod.conf
echo ACCESS_KEY=$(cat ../.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> cron_mod.conf
echo SECRET_KEY=$(cat ../.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> cron_mod.conf
echo REGION=$(cat ../.aws/config | grep region | awk -F'= ' '{print $2}') >> cron_mod.conf
echo SENSOR_NO=$(cat ./iot_prov_config | grep SENSOR_NO | awk -F'=' '{print $2}') >> cron_mod.conf
echo S3BUCKET=$(cat ./iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}') >> cron_mod.conf
echo PREFIX_IN=$(cat ./iot_prov_config | grep PREFIX_IN | awk -F'=' '{print $2}') >> cron_mod.conf
echo TRIGGER_SELECT=$(cat ./iot_prov_config | grep TRIGGER_SELECT | awk -F'=' '{print $2}') >> cron_mod.conf

echo >> cron_mod.conf
echo @reboot ~/.profile >> cron_mod.conf
echo @reboot python ~/main.py >> cron_mod.conf
echo @reboot python ~/emr_rec.py >> cron_mod.conf

# adding .profile
echo >> ../.profile
echo export HOST_ENDPOINT=$(jq -r '.endpointAddress' < ./end_point.json) >> ../.profile
echo export CACERT=./cert/AmazonRootCA1.pem >> ../.profile
echo export CLIENTCERT=./cert/${THING_NAME}-certificate.pem.crt >> ../.profile
echo export CLIENTKEY=./cert/${THING_NAME}-private.pem.key >> ../.profile
echo export  >> ../.profile
echo export TOPIC_DETECT=$(cat ./iot_prov_config | grep TOPIC_DETECT | awk -F'=' '{print $2}') >> ../.profile
echo export  >> ../.profile
echo export ACCESS_KEY=$(cat ../.aws/credentials | grep aws_access_key_id | awk -F'= ' '{print $2}') >> ../.profile
echo export SECRET_KEY=$(cat ../.aws/credentials | grep aws_secret_access_key | awk -F'= ' '{print $2}') >> ../.profile
echo export REGION=$(cat ../.aws/config | grep region | awk -F'= ' '{print $2}') >> ../.profile
echo export SENSOR_NO=$(cat ./iot_prov_config | grep SENSOR_NO | awk -F'=' '{print $2}') >> ../.profile
echo export S3BUCKET=$(cat ./iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}') >> ../.profile
echo export PREFIX_IN=$(cat ./iot_prov_config | grep PREFIX_IN | awk -F'=' '{print $2}') >> ../.profile
echo export TRIGGER_SELECT=$(cat ./iot_prov_config | grep TRIGGER_SELECT | awk -F'=' '{print $2}') >> ../.profile

crontab ./cron_mod.conf
