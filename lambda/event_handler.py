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
        # Get formatted pagerduty message
        pagerdutyMessage = message_formatter.format(event)
        jsonPagerdutyMessage = json.JSONEncoder().encode(pagerdutyMessage)
        logger.info(jsonPagerdutyMessage)

        # Send pagerdutyMessage to SNS
        client = boto3.client('sns')
        snsResp = client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=jsonPagerdutyMessage,
            Subject=pagerdutyMessage['NewStateValue'] + ': "' + pagerdutyMessage['AlarmName'] + '" in ' + pagerdutyMessage['Region']
        )
        response['status'] = 'SUCCESS'
        response['pagerdutyMessage'] = snsResp
    except Exception as e:
        logger.error(e)
        response['status'] = 'FAILED'
        response['pagerdutyMessage'] = 'Failed to publish pagerdutyMessage to SNS Topic'
    logger.info(response)
    return response
