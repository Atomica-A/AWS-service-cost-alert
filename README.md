# AWS-service-cost-alert

A simple AWS Lambda function that checks your daily AWS costs using the Cost Explorer API and sends a Telegram message if there’s any usage. It helps track spending and avoid exceeding the Free Tier.

How It Works

    Lambda runs daily (scheduled via EventBridge).

    It queries Cost Explorer for today’s cost.

    If cost > 0, it sends a Telegram alert.

Setup

    Create a Telegram Bot

        Use @BotFather in Telegram → get BOT_TOKEN

        Get your CHAT_ID

    Create Lambda Function

        Runtime: Python 3.9+

        Upload lambda_function.py

        Add environment variables:

            TELEGRAM_TOKEN = your bot token

            CHAT_ID = your Telegram chat ID

    Add IAM Permission

        Lambda needs ce:GetCostAndUsage

    Schedule with EventBridge

        Set a daily cron rule → trigger Lambda
