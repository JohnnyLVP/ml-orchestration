import json,os
from botocore.vendored import requests
from utils.dynamo_db import DBManager
from utils.orchestrator_utils import OrchestratorManager
from constants.process_stages_enum import PipelineStages
from constants.db_status_enum import DBStatus
from constants.db_tables_enum import DBTables

def lambda_handler(event, context):
    '''

    :param event:
    :param context:
    :return:
    '''
    print(event)
    try:
        # process campaign update message
        process_update_dbtable(event)
        process_update_message(event)

    except Exception as e:
        print("Exception in process_campaign_update_notif lambda: {}".format(e))
        raise e

def process_update_dbtable(event):
    '''

    :param event:
    :return:
    '''
    db_manager = DBManager()
    mlo_manager = OrchestratorManager()
    item = {}

    try:
        item['uuid'] = event['uuid']
        item['timestamp'] = mlo_manager.get_current_timestamp()
        item['stage'] = PipelineStages.request
        item['status'] = DBStatus.pending
        item['reason'] = None

        db_item = mlo_manager.format_db_item(item)
        print("Following item is been writed: {}".format(db_item))

        db_tablename = "{}-{}".format(DBTables.logs,event['env'])

        db_manager.put_item(db_tablename,db_item)
    except Exception as e:
        print("Exception ocurred : {}".format(str(e)))

def process_update_message(event):
    '''

    :param event:
    :return:
    '''
    try:
        message_item = json.loads(event)
        payload = message_item['item']['payload']
        payload['codpais'] = message_item['country']
        payload['aniocampana'] = message_item['campaign']
        response = requests.post(
                        message_item['info']['endpoint'],
                        data = json.dumps(payload))
        print("response: {}".format(response))
        print("response content: {}".format(response.content))

    except Exception as e:
        print("{}".format(e))

    return response