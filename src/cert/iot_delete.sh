#!/bin/bash
THING_NAME=$(cat ./iot_prov_config | grep THING_NAME | awk -F'=' '{print $2}')
CERT_ARN=$(jq -r '.certificateArn' < create-keys-and-certificate.json)

# detach policy to the certificate
aws iot detach-policy --policy-name "${THING_NAME}_subscribe" --target ${CERT_ARN}

delcert=$(cat ./create-keys-and-certificate.json | grep certificateArn | awk -F'/' '{print $2}' | awk -F'"' '{print $1}')
aws iot update-certificate  --certificate-id ${delcert}   --new-status INACTIVE
aws iot detach-thing-principal --thing-name ${THING_NAME} --principal ${CERT_ARN}
aws iot delete-certificate --certificate-id ${delcert}

aws iot delete-thing --thing-name ${THING_NAME}

aws iot delete-policy --policy-name "${THING_NAME}_subscribe"