import json
import os
from utils.step_function import StepFunctionsManager
from utils.orchestrator_utils import OrchestratorManager
from utils.s3 import S3Manager
from utils.sns import SNSManager
from utils.orchestrator_utils import OrchestratorManager
from constants.common_constants import CommonConstants

'''
Environment Variables:
    PATH_NAME: ml-orchestration/algorithm_list.json
    STATE_MACHINE_ARN: arn:aws:states:us-east-1:639556434474:stateMachine:SF-MLO-DEV
    BUCKET_NAME: belc-bigdata-models-dlk-dev
    DY_TABLE_NAME: DY-MLO-FinishedTraining-DEV
    ARN_SNS_TOPIC: 
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

        can_trigger_step = 

        response = sf_manager.execute_step_functions(message)
    except Exception as e:
        print('Exception ocurred: {}'.format(e))

    return response


def can_submit_to_process(sf_manager, execution_type):
    """
    this function checks if we can submit the process to the pipeline or not. It does checks like check if the process
    is requesting either Predict or Train pipeline. It also sees if the number of execution are not overwhelming for the
    pipeline.
    :param sf_manager: step function manager
    :param pipeline: Predict or Train
    :return: boolean
    """
    if execution_type == RecommenderUtils.PREDICT:
        max_exec_allowed = int(os.environ['MAX_SECUENTIAL_EXECUTIONS_ALLOWED'])
    elif execution_type == RecommenderUtils.TRAIN:
        max_exec_allowed = int(os.environ['MAX_DISTRIBIUTED_EXECUTIONS_ALLOWED'])
    
    search_prefix = RecommenderUtils.get_request_search_prefix(pipeline)
    exec_ids = sf_manager.get_running_sf_ids()

    print("search_prefix: {}".format(search_prefix))
    print("exec_ids: {}".format(exec_ids))
    running = sum(idx.startswith(search_prefix) for idx in exec_ids)
    return running < max_exec_allowed


def send_updates_info(message):

    sns_manager = SNSManager(os.environ['REGION_NAME'])
    mlo_manager = OrchestratorManager()
    body = {}

    try:
        body['uuid'] = message['uuid']
        body['timestamp'] = mlo_manager.get_current_timestamp()
        body['info'] = {}
        body['info']['algoritmh'] = message['info']['algoritmo']
        body['info']['codpais'] = message['country']
        body['info']['aniocampana'] = message['campaign']
        body['message_type'] = CommonConstants.sns_update_filter

        response = sns_manager.publish_message(body,
                                               os.environ['ARN_SNS_TOPIC'])

    except Exception as e:
        print("An exception has ocurred: {}".format(str(e)))

'''
def get_json_list():
    try:
        s3_bucket = os.environ['BUCKET_NAME']
        file_path = os.environ['PATH_NAME']
        s3_manager = S3Manager()
        alg_list = s3_manager.get_file_object(s3_bucket, file_path)

    except Exception as e:
        print("Exception ocurred: {}".format(e))

    return json.loads(alg_list)
'''

def get_message_elements(event):
    message = json.loads(event['Records'][0]['body'])
    execution_order = message['init_process']
    process_type = message['process_type']
    
    s3_bucket = os.environ['BUCKET_NAME']
    file_path = os.environ['PATH_NAME']
    try:
        mlo_manager = OrchestratorManager()
        algorithm_list = mlo_manager.get_json_list(s3_bucket, file_path)
        # print(algorithm_list['Process']['DistribuitedProcess'])
        message['uuid'] = mlo_manager.get_uuid()
        if execution_order < len(algorithm_list['Process'][process_type]):
            message['info'] = algorithm_list['Process'][process_type][execution_order]

    except Exception as e:
        print("Exception ocurred: {}".format(e))
    return message
