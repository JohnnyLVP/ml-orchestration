import uuid
import time

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