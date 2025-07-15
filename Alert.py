import boto3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import os

#Environment variables
BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def lambda_handler(event, context):
    # IST time
    ist = ZoneInfo("Asia/Kolkata")
    today = datetime.now(ist).date()

    # Connect to Cost Explorer
    client = boto3.client('ce', region_name='us-east-1')

    #Fetch cost grouped by service
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': today.isoformat(),
            'End': (today + timedelta(days=1)).isoformat()
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
    )

    # Total cost
    cost_amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    total_cost = round(float(cost_amount), 2)

    # Message
    if total_cost > 0:
        message = (
            f" AWS Cost for {today} \n"
            f" You've spent: '${total_cost:.2f}' today.\n"
            f" Check AWS usage - It may exceed free tier."
        )
            
    else:
        message = f"AWS services cost report for {today}: '${total_cost:.2f}'"

    # Send to telegram 
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

    return {
        'statusCode': 200,
        'body': f"Cost ${total_cost:.2f} sent to telegram."
    }

