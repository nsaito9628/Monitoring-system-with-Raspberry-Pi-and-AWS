#!/bin/bash

S3BUCKET=$(cat ./iot_prov_config | grep S3BUCKET | awk -F'=' '{print $2}')

aws s3 rm s3://$S3BUCKET/img --recursive
aws s3 rm s3://$S3BUCKET/Place1 --recursive
aws s3 rm s3://$S3BUCKET/Place2 --recursive
aws s3 rm s3://$S3BUCKET/Place3 --recursive
aws s3 rm s3://$S3BUCKET/Place4 --recursive
aws s3 rm s3://$S3BUCKET/css --recursive
aws s3 rm s3://$S3BUCKET/index.html

aws s3 rb s3://$S3BUCKET