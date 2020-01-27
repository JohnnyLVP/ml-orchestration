import json,os
import uuid
from constants.common_constants import CommonConstants
from utils.sns import SNSManager

'''
    Environment Variables
        REGION_NAME: us-east-1
        TOPIC_ARN: arn:aws:sns:us-east-1:639556434474:SNS-MLO-Topic-DEV
'''

def lambda_handler(event, context):
    
    print(json.dumps(event))
    topic_arn = os.environ['TOPIC_ARN']
    try:
        message = event['Records'][0]['Sns']['Message']
        message_item = json.loads(message)
        response_process = process_mlo_notification(message_item,topic_arn)
        return response_process
    except Exception as e: 
        print("Exception in sns notification: {}",format(e))

def get_hash_uuid():
    uniq_id = str(uuid.uuid4())
    flow_id = "{}".format(uniq_id)
    return flow_id

def process_mlo_notification(message,topic_arn):
    
    region_name = os.environ['REGION_NAME']
    sns_manager = SNSManager(region_name)
    #Create Process Notification
    try:
        process_message = dict(message)
        process_message["message_type"] = CommonConstants.sns_process_filter
        process_message["uuid"] = get_hash_uuid()
        response = sns_manager.publish_message(process_message,topic_arn)
    except Exception as e:
        print("Exception in publishing message to SNS: {}".format(e))
    
    return response
    