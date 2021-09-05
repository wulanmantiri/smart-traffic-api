import json
import boto3
import os


RESPONSE_HEADERS =  {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def format_error_resp(error_message, status_code=400):
    return {
        'statusCode': status_code,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps({
            'error': error_message,
        }),
    }


def format_success_resp(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps(response_body),
    }


def get_dashboard_embed_url(event, _):
    account_id = os.environ["AWS_ACCOUNT_ID"]
    dashboard_id = os.environ["DASHBOARD_ID"]
    qs_client = boto3.client('quicksight', region_name="us-east-1")
    try:
        response = qs_client.get_dashboard_embed_url(
            AwsAccountId=account_id,
            DashboardId=dashboard_id,
            IdentityType='ANONYMOUS',
            SessionLifetimeInMinutes=60,
            Namespace='default',
        )
        return format_success_resp({
            'embed_url': response['EmbedUrl'],
            'request_id': response['RequestId'],
        })
    except Exception as e:
        return format_error_resp(f'Error {str(e)} occurred.')
