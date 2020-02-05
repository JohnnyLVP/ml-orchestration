import json


def lambda_handler(event, context):
    print(json.dumps(event))

    try:

        message = get_message_elements()

    except Exception as e: 
