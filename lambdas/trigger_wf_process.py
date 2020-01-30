import json
import os
from utils.step_function import StepFunctionsManager
from utils.orchestrator_utils import OrchestratorManager
from utils.s3 import S3Manager

'''
Environment Variables:
    PATH_NAME: ml-orchestration/algorithm_list.json
    STATE_MACHINE_ARN: arn:aws:states:us-east-1:639556434474:stateMachine:SF-MLO-DEV
    BUCKET_NAME: belc-bigdata-models-dlk-dev
    DY_TABLE_NAME: DY-MLO-FinishedTraining-DEV
'''

def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))

    try:
        message = get_message_elements(event)
        response = trigger_step_function(message)

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


def get_json_list():
    try:
        s3_bucket = os.environ['BUCKET_NAME']
        file_path = os.environ['PATH_NAME']
        s3_manager = S3Manager()
        alg_list = s3_manager.get_file_object(s3_bucket, file_path)

    except Exception as e:
        print("Exception ocurred: {}".format(e))

    return json.loads(alg_list)


def get_message_elements(event):
    message = json.loads(event['Records'][0]['body'])
    execution_order = message['init_process']
    process_type = message['process_type']

    try:
        mlo_manager = OrchestratorManager()
        algorithm_list = get_json_list()
        # print(algorithm_list['Process']['DistribuitedProcess'])
        message['uuid'] = mlo_manager.get_uuid()
        if execution_order < len(algorithm_list['Process'][process_type]):
            message['info'] = algorithm_list['Process'][process_type][execution_order]

    except Exception as e:
        print("Exception ocurred: {}".format(e))
    return message

