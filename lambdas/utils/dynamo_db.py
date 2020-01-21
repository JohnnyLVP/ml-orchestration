import boto3
import botocore


class DBManager:

    def __init__(self):
        self.dynamo_client = boto3.client("dynamodb")

    def put_item(self, table_name, item):
        """
        this method updates the dynamo db with new items
        :param table_name: table name
        :param item: item to be put in that table
        :return: boolean (success or failed)
        """
        status = True
        try:
            res = self.dynamo_client.put_item(TableName=table_name, Item=item)
            print("Updated the DB successfully!")
        except botocore.exceptions.ClientError as e:
            print("Failed while updating the status to the database: " + str(e))
            status = False

        return status

    def get_item(self, table_name, key):
        """
        this method fetches an item from dynamoDB
        :param table_name: table name
        :param key: item key
        :return: item / record from dynamodb
        """
        response = {}
        try:
            response = self.dynamo_client.get_item(TableName=table_name, Key=key)
        except botocore.exceptions.ClientError as e:
            print("Failed while querying the database: " + str(e))

        return response

    def get_item_list(self, table_name, key, value, ascending_order=False):
        """
        this method fetches a list of items from the dynamo tables
        :param table_name: table name
        :param key: item key
        :param value: where condition value
        :param ascending_order: boolean
        :return: list of items
        """
        response = {}

        try:
            response = self.dynamo_client.query(
                TableName=table_name,
                ExpressionAttributeNames={'#{0}'.format(key): key},
                KeyConditionExpression="#{0} = :val".format(key),
                ExpressionAttributeValues={':val': {'S': value}},
                ScanIndexForward=ascending_order
            )
        except botocore.exceptions.ClientError as e:
            print("Failed while running the query method on the database: " + str(e))
            response['Items'] = []
        return response['Items']
