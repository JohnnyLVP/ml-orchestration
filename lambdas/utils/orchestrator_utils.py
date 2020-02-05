import uuid
import time
from utils.sns import SNSManager
from constants.common_constants import CommonConstants


class OrchestratorManager:

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
    def get_process_status_updates(self,region_name, update_topic_arn, uniq_id, proc_stage, proc_status, failure_reason = None):
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