import json
import os
import requests
from aws_lambda_powertools.utilities.typing import LambdaContext

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

def lambda_handler(event, context: LambdaContext):
    try:
        body = json.loads(event.get("body", "{}"))
        code = body.get("code")

        # Exchange code for access token
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.getenv("REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )

        token_data = token_response.json()

        # Fetch user info
        user_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

        user_info = user_response.json()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Hi {user_info['name']}", "user": user_info}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }