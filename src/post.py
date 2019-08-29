import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event, context):
    """
    Args:
        event (dict):
        context (context): LambdaのContext
    """
    params = json.loads(event['body'])
    logger.info(params)
    response = {
        'result': 'ok',
        'param1': params.get('param1'),
        'param2': params.get('param2')
    }

    if str(type(context)) == '<class \'__main__.FakeLambdaContext\'>':
        # invoked by serverelss command
        logger.info(response)

        return
    else:
        # invoked via API Gateway
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Authorization, Content-Type'
            },
            'body': json.dumps(response),
            'isBase64Encoded': False
        }
