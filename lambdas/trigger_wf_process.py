import json
import os
from utils.step_function import StepFunctionsManager
from utils.orchestrator_utils import OrchestratorManager
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
    MAX_SECUENTIAL_EXECUTIONS_ALLOWED: 1
    MAX_DISTRIBIUTED_EXECUTIONS_ALLOWED: 3
'''


def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))

    try:

        response = trigger_step_function(event)

    except Exception as e:
        print("Exception: {}".format(e))

    return response


def trigger_step_function(event):
    """
        Has to do the following things:
            - trigger the step function
            - write info in dynamo table
            - validate if is able to submit the process
    """
    message = get_message_elements(event)

    try:

        notif_response = send_updates_info(message)

        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        sf_manager = StepFunctionsManager(state_machine_arn)

        can_trigger_step = can_submit_to_process(
            sf_manager, message['process_type'])

        if not can_trigger_step:
            return False

        del_status = delete_message_from_sqs(event)

        if not del_status:
            raise Exception("Failed to delete message from SQS")

        step_prefix = OrchestratorManager.get_request_search_prefix(
            message['process_type'])
        response = sf_manager.execute_step_functions(message, step_prefix)

    except Exception as e:
        print('Exception ocurred: {}'.format(e))

    return response


def can_submit_to_process(sf_manager, execution_type):

    if execution_type == OrchestratorManager.SECUENTIAL:
        max_exec_allowed = int(os.environ['MAX_SECUENTIAL_EXECUTIONS_ALLOWED'])
    elif execution_type == OrchestratorManager.DISTRIBUITED:
        max_exec_allowed = int(os.environ['MAX_DISTRIBIUTED_EXECUTIONS_ALLOWED'])

    search_prefix = OrchestratorManager.get_request_search_prefix(
        execution_type)
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

    return response


def get_message_elements(event):
    message = json.loads(event['Records'][0]['body'])
    execution_order = message['init_process']
    process_type = message['process_type']

    s3_bucket = os.environ['BUCKET_NAME']
    file_path = os.environ['PATH_NAME']
    try:
        mlo_manager = OrchestratorManager()
        algorithm_list = mlo_manager.get_json_list(s3_bucket, file_path)
        message['uuid'] = mlo_manager.get_uuid()
        if execution_order < len(algorithm_list['Process'][process_type]):
            message['info'] = algorithm_list['Process'][process_type][execution_order]

    except Exception as e:
        print("Exception ocurred: {}".format(e))
    return message


def delete_message_from_sqs(event):
    """
    this function deletes messages from sqs
    :param event: event that caused invocation of lambda.
    :return: boolean
    """
    try:
        message = event['Records'][0]
        receipt_handle = message['receiptHandle']
        sqs_manager = SQSManager(message['eventSourceARN'])
        delete_status = sqs_manager.delete_message(receipt_handle)
        print("message deletion status from SQS: {}".format(delete_status))
        return delete_status
    except Exception as e:
        print("Exception: {}".format(e))
    return False
