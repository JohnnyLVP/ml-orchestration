import boto3
import botocore
import json
import time

class SNSManager:

    def __init__(self, region_name):
        self.sns_client = boto3.client('sns', region_name)
        
    def publish_message(self, message_hash, topic_arn, options_hash=dict()):
        """
        this method publishes messages to SNS
        :param message_hash: actual message
        :param topic_arn: sns topic arn
        :param options_hash: hash code
        :return: HTTP status code of the request
        """
        message = json.dumps(message_hash)
        subject = self.get_subject()
        response = {}
        status_code = 200
        
        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject,
                MessageStructure='String',
                MessageAttributes={
                        'message_type': {
                            'DataType': 'String',
                            'StringValue': message_hash['message_type']
                        }
                }
            )
            print("Publish message response: "+json.dumps(response))
            status_code = response['ResponseMetadata']['HTTPStatusCode']
        except botocore.exceptions.ClientError as e:
            print("Failed while publishing the data to SNS topic: "+ str(e))
       	    status_code = int(e.response['ResponseMetadata']['HTTPStatusCode'])

        return status_code 
        
    def get_subject(self):
        subject = "auto-generated subject {}".format(round(time.time() * 1000))
        return subject
