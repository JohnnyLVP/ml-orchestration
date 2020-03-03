import json
import os
from constants.common_constants import CommonConstants
from constants.regular_constants import country, campaign, env, message_type, process_type, init_process
from utils.orchestrator_utils import OrchestratorManager
from utils.sns import SNSManager

process_type = [OrchestratorManager.DISTRIBUITED, OrchestratorManager.SECUENTIAL]
init_index = 0

def lambda_handler(event, context):
    '''

    :param event:
    :param context:
    :return:
    '''
    print(json.dumps(event))
    topic_arn = os.environ['TOPIC_ARN']
    message_item = {}

    try:
        message = event['Records'][0]['Sns']['Message']
        message_item[country] = json.loads(message)['codPais']
        message_item[campaign] = json.loads(message)['anioCampania']

        response = notif_status_notification(message_item, topic_arn, process_type)
        print('Sent notification status: {}'.format(response))

    except Exception as e:
        print("Exception in sns notification: {}", format(e))


def notif_status_notification(message, sns_topic, process_list):
    
    notif_validation = {}
    try:
        for key in process_list:
            response_process = process_mlo_notification(
                message, sns_topic, key)
            if response_process:
                notif_validation[key] = True
            else:
                notif_validation[key] = False
    except Exception as e: 
        print("Exception has ocurred: {}", format(str(e)))

    return notif_validation

def process_mlo_notification(message, topic_arn, process_type):
    '''

    :param message:
    :param topic_arn:
    :param process_type:
    :return:
    '''

    region_name = os.environ['REGION_NAME']
    sns_manager = SNSManager(region_name)

    try:
        process_message = dict(message)
        process_message[env] = os.environ['ENV']
        process_message[message_type] = CommonConstants.sns_process_filter
        process_message[process_type] = process_type
        process_message[init_process] = init_index
        response = sns_manager.publish_message(process_message, topic_arn)
    except Exception as e:
        print("Exception in publishing message to SNS: {}".format(e))

    return response
