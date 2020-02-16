import json

'''
    - Cambair status de 0 a 1 en el json.
    - Send notification to process if success
    - Send notification to update success or failed. 
    
'''

def lambda_handler(event, context):

    print(json.dumps(event))
