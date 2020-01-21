import boto3
import botocore

class SQSManager:
    
    def __init__(self, queue_arn):
        self.client = boto3.client('sqs')
        self.queue_url = self.get_queue_url_from_arn(queue_arn)
        
    def get_queue_url_from_arn(self, queue_arn):
        """
        This function is used to convert arn to url of sqs
        :param queue_arn: sqs arn
        :return: generated url of sqs from arn
        """
        queue_arn_comp = queue_arn.split(':')
        queue_url = 'https://' + queue_arn_comp[3] + '.queue.amazonaws.com/' + queue_arn_comp[4] + '/' + queue_arn_comp[5]
        
        return queue_url
    
    def delete_message(self, receipt_handle):
        """
        This function is used to delete message from sqs queue.
        :param receipt_handle: receipt of the message
        :return: boolean (success or fail)
        """
        try:
            # Delete received message from queue
            self.client.delete_message(QueueUrl = self.queue_url, ReceiptHandle = receipt_handle)
            return True
        except botocore.exceptions.ClientError as e:
            print('Exception occurred while deleting the message from queue: {}'.format(e))
        return False
