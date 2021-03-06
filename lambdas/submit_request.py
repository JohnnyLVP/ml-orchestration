import json
import os
#botocore is executing from the AWS lambda layer
from botocore.vendored import requests
from constants.regular_constants import mlo_uuid, request_ok_status,request_created_status, none_failure_reason, request_status, uuid, process_info, status, country, campaign, info, algortihm_payload, endpoint, stage, created_at, failure_reason
from utils.orchestrator_utils import OrchestratorManager
from constants.process_stages_enum import PipelineStages
from constants.db_status_enum import DBStatus
from constants.common_constants import CommonConstants
from constants.process_stages_enum import PipelineStages


def lambda_handler(event, context):
    '''

    :param event:
    :param context:
    :return:
    '''
    print(event)
    aws_region = os.environ['REGION_NAME']
    update_topic = os.environ['SNS_TOPIC_ARN']
    mlo_manager = OrchestratorManager()
    event[process_info] = {}
    
    try:
        event[process_info][stage] = PipelineStages.request
        event[process_info][created_at] = OrchestratorManager.get_current_timestamp()

        # process campaign update message
        response = get_response_train_request(event)

        print(response)
        print(response.content)   

        if response.status_code in [request_ok_status, request_created_status]:
            event[request_status] = CommonConstants.request_succeded
            event[process_info][status] = DBStatus.submitted 
            event[process_info][failure_reason] = none_failure_reason
        else:
            event[request_status] = CommonConstants.request_failed
            event[process_info][status] = DBStatus.failed
            event[process_info][failure_reason] = none_failure_reason

        mlo_manager.get_process_status_updates(
            region_name=aws_region,
            update_topic_arn=update_topic,
            uniq_id=event[uuid],
            proc_stage=PipelineStages.request,
            proc_status=DBStatus.submitted,
            failure_reason_message=event[process_info][failure_reason]
        )

    except Exception as e:
        print("Exception in process_campaign_update_notif lambda: {}".format(str(e)))
        event[process_info][failure_reason] = str(e)[:150]
        mlo_manager.get_process_status_updates(
            region_name=aws_region,
            update_topic_arn=update_topic,
            uniq_id=event[uuid],
            proc_stage=PipelineStages.request,
            proc_status=DBStatus.failed,
            failure_reason_message=event[process_info][failure_reason]
        )
        event[request_status] = CommonConstants.request_failed
        event[process_info][status] = DBStatus.failed

    return event


def get_response_train_request(event):
    '''

    :param event:
    :return:
    '''
    message_item = event
    payload = {}
    
    try:
        payload[country] = message_item[country]
        payload[campaign] = message_item[campaign]
        payload[mlo_uuid] = message_item[uuid]
        payload.update(message_item[info][algortihm_payload])

        print("payload:{}".format(payload))

        response = requests.post(
            message_item[info][endpoint],
            data=json.dumps(payload))

    except Exception as e:
        print("Request issues: {}".format(e))

    return response
