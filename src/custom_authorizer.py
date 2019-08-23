import logging

from src.utils.env import get_secret_env

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

valid_token = get_secret_env('API_AUTH_KEY')
valid_ip_address = list(map(lambda ip: ip.strip(), get_secret_env('API_ALLOW_IP').split(',')))


def main(event, context):
    valid = False
    source_ip = event['headers']['X-Forwarded-For'].split(',')[0].strip()
    token = event['headers']['Authorization']

    if valid_token == token and source_ip in valid_ip_address:
        valid = True
        logger.info('request is valid')
    else:
        logger.info('request is not valid')

    if valid:
        return {
            'principalId': 1,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': 'arn:aws:execute-api:*:*:*/*/*/*'
                    }
                ]
            }
        }
    else:
        return {
            'principalId': 1,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': '*',
                        'Effect': 'Deny',
                        'Resource': 'arn:aws:execute-api:*:*:*/*/*/'
                    }
                ]
            }
        }
