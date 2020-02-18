import json
from utils.orchestrator_utils import OrchestratorManager
from utils.sns import SNSManager

'''
    - Cambair status de 0 a 1 en el json.
    - Send notification to process if success
    - Send notification to update success or failed. 
    
'''

def lambda_handler(event, context):
    
    print(json.dumps(event))
    sns_manager = SNSManager(os.environ['REGION'])
    
    try:
        
        if event['process_info']['stage'] == 'ALGORITHM' and event['process_info']['status'] == 'SUCCEEDED':
            #SNS message with init_process +1 
            #process message 
            #updates message 
        
        elif event['process_info']['stage'] == 'ALGORITHM' and event['process_info']['status'] == 'FAILED':
            #SNS message with init_process +1 with failed
            #process message
            #updates message 

    except Exception, e:
        raise e


def post_process_message(event, sns_manager):
    
    mlo_manager = OrchestratorManager()
    
    s3_bucket = os.enviorn['S3_BUCKET']
    file_path = os.environ['PATH_NAME']

    algorithm_list = mlo_manager.get_json_list(s3_bucket,file_path)
    process_message = {}
    #{"country": "CR", "campaign": "202001", "env": "DEV", "message_type": "process", "process_type": "SecuentialProcess", "init_process": 0}
    try:
        process_message['country'] = event['country']
        process_message['campaign'] = event['campaign']
        process_message['env'] = event['env']
        process_message['message_type'] = event['message_type']
        process_message['process_type'] = event['process_type']
        
        current_execution_order = event['init_process']
        if current_execution_order < len(algorithm_list['Process'][event['process_type']])
            process_message['init_process'] = current_execution_order + 1
        
        response = sns_manager.publish_message(process_message, os.environ['SNS_TOPIC_ARN'])

    except Exception, e: 
        print("Exception has ocurred: {}".format(e))
    
def post_updates_message(event):
    #"{\"uuid\": \"59ec7fb6-54ba-4335-b747-f4e070bd2c5b\", \"timestamp\": 1580933339888, \"stage\": \"REQUEST\", \"status\": \"FAILED\", \"failure_reason\": \"None\", \"message_type\": \"updates\"}",
    update_message = {}
    try:
        update_message['uuid'] = event['uuid']
        update_message['timestamp'] = event['process_info']['created_at']
        update_message['']

    