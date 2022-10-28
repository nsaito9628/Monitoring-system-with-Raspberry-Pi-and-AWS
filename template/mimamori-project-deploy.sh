#!/bin/bash

BUCKET_NAME=$(cat ../../cert/iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}')

#sudo pip3 install -U awscli
/usr/local/bin/aws s3 cp ./index.html s3://${BUCKET_NAME}
/usr/local/bin/aws s3 cp ./css/ s3://${BUCKET_NAME}/css --recursive
/usr/local/bin/aws s3 cp ./Place1/ s3://${BUCKET_NAME}/Place1 --recursive
/usr/local/bin/aws s3 cp ./Place2/ s3://${BUCKET_NAME}/Place2 --recursive
/usr/local/bin/aws s3 cp ./Place3/ s3://${BUCKET_NAME}/Place3 --recursive
/usr/local/bin/aws s3 cp ./Place4/ s3://${BUCKET_NAME}/Place4 --recursive
/usr/local/bin/aws s3 cp ./img/ s3://${BUCKET_NAME}/img --recursive

exit 0