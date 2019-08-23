import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event, context):
    """
    Args:
        event (dict): keys(location, keyword)
        context (context): LambdaのContext
    """
    logger.info(event)
    response = {
        'result': 'ok',
        'param1': event.get('param1'),
        'param2': event.get('param2')
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
                'Access-Control-Allow-Headers': 'Authorization'
            },
            'body': json.dumps(response),
            'isBase64Encoded': False
        }
