# -*- coding:utf-8 -*-
import os
from gen_main_html import Gen_main
from gen_each_html import Gen_each


main = Gen_main()
each = Gen_each()


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


    trigger_select = (int(input("Input trigger type if to use sensor is '0' else motion detection is '1': ")))
    S3Bucket = input("Input S3 bucket name to upload mp4 files: ")
    AWS_account = input("Input your AWS account Id : ")


    return project_name, num_place, place_name, sensor_open_close, S3Bucket, AWS_account, what_num, trigger_select


def config_gen(place_name, S3Bucket, AWS_account, sensor_open_close, what_num, trigger_select):

    config_path = "./src"
    filename_config =  "iot_prov_config"
    Place = "Place" + str(what_num)

    #os.remove(config_path + "/cert/" + filename_config)

    prov_config = f'''THING_NAME={place_name[0]}
TOPIC_DETECT={place_name[0]}/count
S3BUCKET={S3Bucket}
AWS_AccountId={AWS_account}
SENSOR_NO={sensor_open_close[0]}
PREFIX_IN={Place}
TRIGGER_SELECT={trigger_select}'''
     
    with open(config_path + "/cert/" + filename_config, 'w', encoding='utf-8' ) as f: 
            f.write(prov_config) 
    
    return


def template_param_gen(num_place, project_name, place_name, S3Bucket):
    
    place = ""
    
    for index, name in enumerate(place_name):
        if index < num_place - 1 :
            place = place + name + "," 
        elif index >= num_place - 1:
            place = place + name
        
    template_param =f'''AWSTemplateFormatVersion: '2010-09-09'
Transform:
  - AWS::Serverless-2016-10-31
  - Count
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
    Default: {project_name}
  Place:
    Type: String
    Default: {place}
  NumPlace:
    Type: Number
    Default: {str(num_place)}
  OrgBucketName:
    Type: String
    Default: {S3Bucket}
  NameTag:
    Type: String
    Default: {project_name}
############# Fixed #############
  EventPrefix:
    Type: String
    Default: 'emr'
#################################


####################################
Resources:
####################################
'''

    #shutil.copytree("./template/template.yaml", "./template/template.yaml.bak")
    #os.remove("./template/template.yaml")
         
    with open("./template/template_head.txt", 'w', encoding='utf-8' ) as f: 
        f.write(template_param) 


def template_dashboard_gen(project_name, place_name):

    y = [0, 0, 6, 6]
    x = [0, 12, 0, 12]
    body = ""

    header = f'''  CloudWatchDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: {project_name}Dashboard
      DashboardBody: |
                  {{
                      "widgets": [
'''

    for index, name in enumerate(place_name):
        if index > 0:
            body = body + ","    
        body = body + f'''
                            {{
                              "height": 6, 
                              "width": 12,
                              "y": {str(y[index])},
                              "x": {str(x[index])},
                              "type": "metric",
                              "properties": {{
                                  "metrics": [
                                      [ 
                                        "{name}/count", 
                                        "detect_count" 
                                      ]
                                  ],
                                  "view": "timeSeries",
                                  "stacked": false,
                                  "region": "ap-northeast-1",
                                  "title": "{name}",
                                  "period": 60,
                                  "stat": "Sum"
                                }}
                            }}'''
    footer = '''
                        ]
                    }
'''

    template_dashboard = header + body + footer

    with open("./template/template_dashboard.txt", 'w', encoding='utf-8' ) as f: 
        f.write(template_dashboard) 


def comb_template():

    yaml_files = ["./template/template_head.txt", "./template/template_dashboard.txt", "./template/template_body.txt"]

    with open("./template/template.yaml", "w", encoding='utf-8' ) as new_file:
        for name in yaml_files:
            with open(name, "r", encoding='utf-8', errors='ignore') as f:
                new_file.write(f.read())
            

if __name__ == '__main__':
    project_name, num_place, place_name, sensor_open_close, S3Bucket, AWS_account, what_num, trigger_select = input_parameters()
    config_gen(place_name, S3Bucket, AWS_account, sensor_open_close, what_num, trigger_select)
    if what_num == 1:
        template_param_gen(num_place, project_name, place_name, S3Bucket)
        template_dashboard_gen(project_name, place_name)
        comb_template()
        each.gen_each_html(place_name)
        index_body_head = main.gen_body_head(place_name)
        each_body = main.gen_mid_body(place_name)
        main.comb_index(index_body_head, each_body)

