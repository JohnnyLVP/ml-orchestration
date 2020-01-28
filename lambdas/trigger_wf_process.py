import json
import os
from utils.step_functions import StepFunctionsManager
from utils.s3 import S3Manager

'''
Environment Variables:
    PATH_NAME: ml-orchestration/algorithm_list.json
    STATE_MACHINE_ARN: arn:aws:states:us-east-1:639556434474:stateMachine:SF-MLO-DEV
    BUCKET_NAME: belc-bigdata-models-dlk-dev
'''

def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))
    
    try: 
        message = get_message_hash(event)
        #response = trigger_step_function(message)
        get_training_uuid(message)
    except Exception as e:
        print("Exception: {}".format(e))

def trigger_step_function(message):
    
    try:
        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        sf_manager = StepFunctionsManager(state_machine_arn)
        response = sf_manager.execute_step_functions(message)
    except Exception as e:
        print('Exception ocurred: {}'.format(e))
    
    return response
    
    
def get_message_hash(event):
    message = json.loads(event['Records'][0]['body'])
    #message = json.loads(message['Message'])
    return message
    
def get_training_uuid(message):
    
    try:
        s3_bucket = os.environ['BUCKET_NAME']
        file_path = os.environ['PATH_NAME']
        s3_manager = S3Manager()
        json_list = s3_manager.get_file_object(s3_bucket,file_path)
        print(json_list)
    except Exception as e:
        print("Exception ocurred: {}".format(e))
    
    