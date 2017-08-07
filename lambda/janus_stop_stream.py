import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iot = boto3.client('iot')
iot_data = boto3.client('iot-data')


def handler(event, context):
    logger.info(json.dumps(event, sort_keys=True, indent=4))

    thing_name = event['thingName']

    logger.info(thing_name)

    thing_shadow = json.loads(iot_data.get_thing_shadow(thingName=thing_name)['payload'].read().decode('utf-8'))
    logger.info(json.dumps(thing_shadow, indent=2))

    streams = thing_shadow['state']['desired'].get('streams')
    logger.info(f'Currently allocated streams: {streams}')

    # todo: client refcounting so camera could stop streaming if there are no clients
    # streams['current'] = None

    iot_data.update_thing_shadow(
        thingName=thing_name,
        payload=json.dumps({'state': {
            'desired': {
                'streams': streams
            }
        }}).encode('utf-8'))
