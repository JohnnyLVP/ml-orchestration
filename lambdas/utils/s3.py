import boto3
import botocore

class S3Manager:

    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.file_read_response = None

    def does_files_exist(self, s3_file_bucket_map_list):
        file_status = True
        for s3_file_bucket_map in s3_file_bucket_map_list:
            file_path = s3_file_bucket_map["s3_file_path"]
            bucket = s3_file_bucket_map["bucket"]

            try:
                self.file_read_response = self.s3_client.\
                    head_object(Bucket=bucket, Key=file_path)
                print("File: " + file_path + " is present on S3")
            except botocore.exceptions.ClientError as e:
                print("Exception Occurred: " + str(e))
                if e.response['Error']['Code'] == '404':
                    print("File: " + file_path + " is not present on S3")
                    file_status = False
                    break
        
        return file_status

    def get_file_size(self):
        file_size = 0
        if(self.file_read_response and self.file_read_response.get('ContentLength')):
            file_size = self.file_read_response['ContentLength']

        return file_size

    def write_data(self, file_name, bucket, s3_file_path):
        status = True
        try:
            self.s3_client.upload_file(
                Filename=file_name,
                Bucket=bucket,
                Key=s3_file_path
            )
            print("Written the data successfully to S3")
        except botocore.exceptions.ClientError as e:
            print("Exception occurred while writing the data to S3: "+str(e))
            status = False

        return status

    def get_file_object(self, bucket, s3_file_path):

        try:
            result = self.s3_client.get_object(
                Bucket = bucket,
                Key = s3_file_path
            )
            file = result["Body"].read().decode()    
        except botocore.exceptions.ClientError as e:
            print("Exception ocurred while getting file from s3, {}".format(str(e)))
        
        return file