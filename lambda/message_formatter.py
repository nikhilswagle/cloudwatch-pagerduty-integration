import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Format message to be sent to pager duty via SNS.
'''
def format(event):
    message = json.load(open('message.json', 'r'))
    message['Severity'] = __getSeverity(event)
    message['Client'] = 'Amazon Cloudwatch Alarm'
    message['Alarms'] = event['resources']
    message['Title'] = event['detail']['alarmName']
    message['Description'] = event['detail']['configuration']['description'] + '/n' + event['detail']['state']['reason']
    message['Details'] = __getMetricDimensions(event)
    return message

'''
Collects metric dimensions for given alarm
'''
def __getMetricDimensions(event):
    dimensions = {}
    for metric in event['detail']['configuration']['metrics']:
        if 'metricStat' in metric and 'dimensions' in metric['metricStat']['metric']:
            for key, value in metric['metricStat']['metric']['dimensions'].items():
                if key not in dimensions:
                    dimensions[key] = []
                dimensions[key].append(value)
    return dimensions

'''
Figures out severity of the message.
'''
def __getSeverity(event):
    '''
    Implement method if required to figure out severity.
    Default is CRITICAL
    '''
    return 'CRITICAL'
