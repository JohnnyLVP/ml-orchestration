import json,os
from constants.common_constants import CommonConstants
from utils.sns import SNSManager

'''
    Environment Variables
        REGION_NAME: us-east-1
        TOPIC_ARN: arn:aws:sns:us-east-1:639556434474:SNS-MLO-Topic-DEV
'''

process_type = ["DISTRIBUITED_PROCESS", "SECUENTIAL_PROCESS"]

def lambda_handler(event, context):
    
    print(json.dumps(event))
    topic_arn = os.environ['TOPIC_ARN']
    try:
        message = event['Records'][0]['Sns']['Message']
        message_item = {} 
        message_item['country'] = json.loads(message)['codPais']
        message_item['campaign'] = json.loads(message)['anioCampania']
        
        for key in process_type:
            response_process = process_mlo_notification(message_item,topic_arn,key)
        
    except Exception as e: 
        print("Exception in sns notification: {}",format(e))

def process_mlo_notification(message,topic_arn,process_type):
    
    region_name = os.environ['REGION_NAME']
    sns_manager = SNSManager(region_name)
    #Create Process Notification
    try:
        process_message = dict(message)
        process_message["message_type"] = CommonConstants.sns_process_filter
        process_message["process_type"]= process_type
        response = sns_manager.publish_message(process_message,topic_arn)
    except Exception as e:
        print("Exception in publishing message to SNS: {}".format(e))
    
    return response

