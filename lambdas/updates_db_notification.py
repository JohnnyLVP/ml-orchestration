import json
import os
from utils.orchestrator_utils import OrchestratorManager
from utils.dynamo_db import DBManager
from constants.db_tables_enum import DBTables
from constants.regular_constants import *

'''
    DY_INFO_TABLE_NAME: 
    DY_PROCESSING_TABLE_NAME:
'''


def lambda_handler(event, context):
    print(json.dumps(event))

    try:
        message = json.loads(event['Records'][0]['body'])
        dy_tablename, dy_status = update_dynamo_table(message)

        print('Table {db_table} has been updated: {db_status}'.format(
            db_table=dy_tablename,
            db_status=dy_status
        ))

    except Exception as e:
        print('Exception has ocurred: {}'.format(str(e)))

    return (dy_tablename, dy_status)


def update_dynamo_table(message):

    mlo_manager = OrchestratorManager()
    db_manager = DBManager()
    item = {}
    status = True
    try:

        if message.get(info):

            dy_tablename = os.environ['DY_INFO_TABLE_NAME']
            item[uuid] = message[uuid]
            item[timestamp_string] = message[timestamp_string]
            item[info] = str(message[info])

        else:

            dy_tablename = os.environ['DY_PROCESSING_TABLE_NAME']
            item[uuid] = message[uuid]
            item[timestamp_string] = message[timestamp_string]
            item[stage] = message[stage]
            item[status] = message[status]
            item[failure_reason] = message[failure_reason]

        db_items = mlo_manager.format_db_item(message_item=item)

        status = db_manager.put_item(
            table_name=dy_tablename,
            item=db_items)

    except Exception as e:
        print("Exception has ocurred: {}".format(str(e)))
        status = False

    return dy_tablename, status
