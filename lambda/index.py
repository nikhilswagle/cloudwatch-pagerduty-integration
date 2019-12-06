import logging
import event_handler

log = logging.getLogger()
log.setLevel(logging.INFO)

def lambda_handler(event, context):
    return event_handler.handle_event(event, context)
