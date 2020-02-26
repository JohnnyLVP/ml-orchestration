import json, os
import uuid
import time
from utils.sns import SNSManager
from utils.s3 import S3Manager
from constants.common_constants import CommonConstants


class OrchestratorManager:

    DISTRIBUITED = 'DistribuitedProcess'
    SECUENTIAL = 'SecuentialProcess'

    @classmethod
    def get_uuid(self):
        uniq_id = str(uuid.uuid4())
        return "{}".format(uniq_id)

    @classmethod
    def get_current_timestamp(self):
        timestamp = int(time.time() * 1000)
        return timestamp

    @classmethod
    def format_db_item(self, message_item):
        db_item = {}
        for key, value in message_item.items():
            if (isinstance(value, str)):
                db_item[key] = {"S": value}
            elif (isinstance(value, int)):
                db_item[key] = {"N": str(value)}
            elif (isinstance(value, float)):
                db_item[key] = {"N": str(value)}
            elif (not value):
                db_item[key] = {"S": ""}

        return db_item

    @classmethod
    def get_process_status_updates(self,region_name, update_topic_arn, uniq_id, proc_stage, proc_status, failure_reason ):
        sns_manager = SNSManager(region_name)
        item = {}
        try:
            item['uuid'] = uniq_id
            item['timestamp'] = self.get_current_timestamp()
            item['stage'] = proc_stage
            item['status'] = proc_status
            item['failure_reason'] = failure_reason
            item['message_type'] = CommonConstants.sns_update_filter
            
            response = sns_manager.publish_message(
                message_hash = item,
                topic_arn = update_topic_arn
            )

            print("Info sent by sns notification: {}".format(item))
        except Exception as e:
            print("Exception has ocurred: {}".format(str(e)))
    
        return response

    @classmethod
    def get_time_duration(self, start_time):
        curr_time = self.get_current_timestamp()
        duration = int(curr_time) - int(start_time)
        return duration # in millisec
    
    @classmethod
    def get_json_list(self, s3_bucket, file_path):
        try:
            #s3_bucket = os.environ['BUCKET_NAME']
            #file_path = os.environ['PATH_NAME']
            s3_manager = S3Manager()
            alg_list = s3_manager.get_file_object(s3_bucket,file_path)
            
        except Exception as e:
            print("Exception ocurred: {}".format(e))
        
        return json.loads(alg_list)
    
    @classmethod
    def get_request_search_prefix(self, request_type):
        if request_type == OrchestratorManager.DISTRIBUITED:
            return CommonConstants.dist_search_prefix
        elif request_type == OrchestratorManager.SECUENTIAL:
            return CommonConstants.sec_search_prefix
        return None