import json
import os
from utils.orchestrator_utils import OrchestratorManager
from utils.sns import SNSManager
from constants.db_status_enum import DBStatus
from constants.process_stages_enum import PipelineStages
from constants.regular_constants import *
from constants.common_constants import CommonConstants


def lambda_handler(event, context):

    print(json.dumps(event))
    sns_manager = SNSManager(os.environ['REGION'])

    try:
        process_response = post_process_message(event, sns_manager)
        print("Process message was sent: {}".format(process_response))

        update_response = post_updates_message(event, sns_manager)
        print("Update message was sent: {}".format(update_response))

    except Exception as e:
        print("Exception has ocurred while sending the sns message:{}".format(str(e)))


def post_process_message(event, sns_manager):

    mlo_manager = OrchestratorManager()

    s3_bucket = os.environ['S3_BUCKET']
    file_path = os.environ['PATH_NAME']

    algorithm_list = mlo_manager.get_json_list(s3_bucket, file_path)
    process_message = {}
    #{"country": "CR", "campaign": "202001", "env": "DEV", "message_type": "process", "process_type": "SecuentialProcess", "init_process": 0}
    try:
        process_message[country] = event[country]
        process_message[campaign] = event[campaign]
        process_message[env] = event[env]
        process_message[message_type] = event[message_type]
        process_message[process_type] = event[process_type]

        current_execution_order = event[init_process]
        if current_execution_order < len(algorithm_list[list_process][event[process_type]]):
            process_message[init_process] = current_execution_order + 1

            response = sns_manager.publish_message(
                process_message, os.environ['SNS_TOPIC_ARN'])

            return response
            
        else:
            print(
                "Algorithms in execution {execution_type} list has finished the training for country: {country}, campaign: {campaign}".format(
                    execution_type= process_message[process_type],
                    country = process_message[country],
                    campaign = process_message[campaign]
                ))

    except Exception as e:
        print("Exception has ocurred: {}".format(e))

    


def post_updates_message(event, sns_manager):
    #"{\"uuid\": \"59ec7fb6-54ba-4335-b747-f4e070bd2c5b\", \"timestamp\": 1580933339888, \"stage\": \"REQUEST\", \"status\": \"FAILED\", \"failure_reason\": \"None\", \"message_type\": \"updates\"}",
    update_message = {}
    try:
        update_message[uuid] = event[uuid]
        update_message[timestamp_string] = event[process_info][created_at]
        update_message[stage] = PipelineStages.post_process
        update_message[status] = event[process_info][status]
        update_message[failure_reason] = event[process_info][failure_reason]
        update_message[message_type] = CommonConstants.sns_update_filter

        if event[process_info][status] == DBStatus.failed and event[process_info][stage] == PipelineStages.algorithm:
            update_message[algorithm] = event[info][algorithm]

        response = sns_manager.publish_message(
            update_message, os.environ['SNS_TOPIC_ARN'])

    except Exception as e:
        print("Exception has ocurred:{}".format(str(e)))

    return response
