import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Format message to be sent to pager duty via SNS.
'''
def format(event):
    message = json.load(open('message.json', 'r'))
    message['AlarmName'] = event['detail']['alarmName']
    if 'description' in event['detail']['configuration']:
        message['AlarmDescription'] = event['detail']['configuration']['description']
    else:
        message['AlarmDescription'] = event['detail']['alarmName']
    message['AWSAccountId'] = event['account']
    message['NewStateValue'] = event['detail']['state']['value']
    message['NewStateReason'] = event['detail']['state']['reason']
    message['StateChangeTime'] = event['detail']['state']['timestamp']
    message['Region'] = event['region']
    message['OldStateValue'] = event['detail']['previousState']['value']
    message = __updateMessageWithAlarmDetails(event, message)
    return message

'''
Collects required alarm details and updates them into the message to be sent out to pager duty.
'''
def __updateMessageWithAlarmDetails(event, message):
    client = boto3.client('cloudwatch')
    response = client.describe_alarms(
        AlarmNames=[
            event['detail']['alarmName']
        ]
    )
    # Get first item from the response since we are expecting only one alarm
    metricAlarm = response['MetricAlarms'][0]
    message['Trigger']['MetricName'] = metricAlarm['MetricName']
    message['Trigger']['Namespace'] = metricAlarm['Namespace']
    message['Trigger']['Period'] = metricAlarm['Period']
    message['Trigger']['Statistic'] = metricAlarm['Statistic']
    message['Trigger']['ComparisonOperator'] = metricAlarm['ComparisonOperator']
    message['Trigger']['EvaluationPeriods'] = metricAlarm['EvaluationPeriods']
    message['Trigger']['Threshold'] = metricAlarm['Threshold']
    if 'Unit' in metricAlarm:
        message['Trigger']['Unit'] = metricAlarm['Unit']
    if 'TreatMissingData' in metricAlarm:
        message['Trigger']['TreatMissingData'] = metricAlarm['TreatMissingData']
    message['Trigger']['Dimensions'] = metricAlarm['Dimensions']
    return message
