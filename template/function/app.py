import boto3
import os


s3 = boto3.client('s3')

ORG_BACKET = os.environ['ORG_BACKET']

PLACE1 = "Place1"
PLACE2 = "Place2" 
PLACE3 = "Place3" 
PLACE4 = "Place4" 

deploy_file = ["12.mp4",
                "11.mp4",
                "10.mp4",
                "09.mp4",
                "08.mp4",
                "07.mp4",
                "06.mp4",
                "05.mp4",
                "04.mp4",
                "03.mp4",
                "02.mp4",
                "01.mp4"]


def modify_fname(filename, prefix):
    for i in range(len(deploy_file)):
        try:
            if deploy_file[i] == '01.mp4':
                s3.copy_object(Bucket=ORG_BACKET, 
                                Key=prefix+deploy_file[i],
                                CopySource={'Bucket': ORG_BACKET, 
                                            'Key': filename})
                s3.delete_object(Bucket=ORG_BACKET, 
                                Key=filename)
                break
            else:                    
                s3.copy_object(Bucket=ORG_BACKET, 
                                Key=prefix+deploy_file[i], 
                                CopySource={'Bucket': ORG_BACKET, 
                                            'Key': prefix+deploy_file[i+1]})
        except Exception as e:
            pass
    return


def lambda_handler(event, context):
    
    for rec in event['Records']:
        filename = (rec['s3']['object']['key'])
        print(filename)

        if PLACE1 in filename: prefix = PLACE1 + "/"
        if PLACE2 in filename: prefix = PLACE2 + "/"
        if PLACE3 in filename: prefix = PLACE3 + "/"
        if PLACE4 in filename: prefix = PLACE4 + "/"

        modify_fname(filename, prefix)

    return
