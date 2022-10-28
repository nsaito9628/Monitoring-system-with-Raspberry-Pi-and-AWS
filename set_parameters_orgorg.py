# -*- coding:utf-8 -*-
import os
import shutil


def input_parameters():
    project_name = ""
    num_place = 0
    place_name = []
    sensor_open_close = []

    while True:
        what_num = int(input("What number is this place to set RaspberryPi and cam (Allowed values are 1, 2, 3 or 4): "))
        if  0 < what_num < 5: break
        
    if what_num == 1:
        #
        project_name = input("Input project name e.g., room name such as 'MyLiving': ")
        while True:
            num_place = int(input("Input number of places you need to watch over (less than 4): "))
            if  0 < num_place < 5: break

        for i in range(num_place):
            print("Input for Place No." + str(i+1))
            place_name.append(input("Input place name: "))
            sensor_open_close.append(int(input("Input sensor type if normal close is '0' else normal open is '1': ")))
    else:
        print("Input for Place No." + str(what_num))
        place_name.append(input("Input place name: "))
        sensor_open_close.append(int(input("Input sensor type if normal close is '0' else normal open is '1': ")))


    S3Bucket = input("Input S3 bucket name to upload mp4 files: ")


    return project_name, num_place, place_name, sensor_open_close, S3Bucket, what_num


def config_gen(place_name, S3Bucket, sensor_open_close, what_num):

    config_path = "./src"
    filename_config =  "iot_prov_config"
    Place = "Place" + str(what_num)

    #os.remove(config_path + "/cert/" + filename_config)

    prov_config = '''THING_NAME={PLACE_NAME}
TOPIC_DETECT={PLACE_NAME}/count
S3BUCKET={BucketName}
SENSOR_NO={Sensor_NO}
PREFIX_IN={PLACE}
            '''.format(PLACE_NAME = place_name[0],
                        BucketName = S3Bucket,
                        Sensor_NO = sensor_open_close[0],
                        PLACE=Place) 
     
    with open(config_path + "/cert/" + filename_config, 'w', encoding='utf-8' ) as f: 
            f.write(prov_config) 
    
    return


def template_gen(num_place, project_name, place_name, S3Bucket):
    
    place = []
    
    for i in range(4):
        if i < num_place:
            place.append("Default: " + place_name[i])
        elif i >= num_place:
            place.append("#")
        
    template_yaml ='''AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  SAM Template for Watch-Over-Dashboard-and-Cam deployment

Globals:
  Function:
    Runtime: python3.9
    Timeout: 15
    MemorySize: 128
    Architectures:
      - arm64

####################################
Parameters:
############Customizable############
  ProjectName:
    Type: String
    Default: {PROJECT_NAME}
  Place1:
    Type: String
    {PLACE1}
  Place2:
    Type: String
    {PLACE2}
  Place3:
    Type: String
    {PLACE3}
  Place4:
    Type: String
    {PLACE4}
  OrgBucketName:
    Type: String
    Default: {BUCKET_NAME}
  NameTag:
    Type: String
    Default: {PROJECT_NAME}
############# Fixed #############
  EventPrefix:
    Type: String
    Default: 'emr'
#################################

        '''.format(PROJECT_NAME = project_name,
                        PLACE1 = place[0],
                        PLACE2 = place[1],
                        PLACE3 = place[2],
                        PLACE4 = place[3],
                        BUCKET_NAME = S3Bucket)

    #shutil.copytree("./template/template.yaml", "./template/template.yaml.bak")
    #os.remove("./template/template.yaml")
         
    with open("./template/template_head.txt", 'w', encoding='utf-8' ) as f: 
        f.write(template_yaml) 

    yaml_files = ["./template/template_head.txt", "./template/template_body.txt"]

    with open("./template/template.yaml", "w", encoding='utf-8' ) as new_file:
        for name in yaml_files:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                new_file.write(f.read())
            

if __name__ == '__main__':
    project_name, num_place, place_name, sensor_open_close, S3Bucket, what_num = input_parameters()
    config_gen(place_name, S3Bucket, sensor_open_close, what_num)
    if what_num == 1:
        template_gen(num_place, project_name, place_name, S3Bucket)
