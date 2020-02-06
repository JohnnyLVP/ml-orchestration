import json
import os
from botocore.vendored import requests
from constants.regular_constants import *
from utils.orchestrator_utils import OrchestratorManager
from constants.process_stages_enum import PipelineStages
from constants.db_status_enum import DBStatus
from constants.common_constants import CommonConstants



def lambda_handler(event, context):
    #print(json.dumps(event))

    try:
        message = json.loads(event['Records'][0]['body'])

        if message.get('info'):
            print("Write in Info DynamoTable...") #Lambda Trigger process siempre tiene que manda este update
        
        else:
            print("Write in Processing DynamoTable...")
            
    except Exception as e:
        print('Exception has ocurred: {}'.format(str(e)))