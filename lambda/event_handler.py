import logging
import os
import json
import boto3
import message_formatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Handle lambda event
'''
def handle_event(event, context):
    logger.info('EVENT:' + json.dumps(event, default=str))
    response = {}
    try:
        # Get formatted message
        message = message_formatter.format(event)
        jsonMessage = json.dumps(message)
        logger.info(jsonMessage)

        # Send message to SNS
        client = boto3.client('sns')
        snsResp = client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=jsonMessage,
            Subject=message['Title']
        )
        response['status'] = 'SUCCESS'
        response['message'] = snsResp
    except Exception as e:
        logger.error(e)
        response['status'] = 'FAILED'
        response['message'] = 'Failed to publish message to SNS Topic'
    logger.info(response)
    return response
