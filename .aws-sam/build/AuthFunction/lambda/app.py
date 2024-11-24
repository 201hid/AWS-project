import json
import os
import requests
from aws_lambda_powertools.utilities.typing import LambdaContext

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


def lambda_handler(event, context: LambdaContext):
    try:
        # Log incoming event for debugging
        print("Incoming event:", json.dumps(event))

        path = event.get("path")
        http_method = event.get("httpMethod")

        # Handle OAuth redirection request
        if path == "/auth/google" and http_method == "POST":
            return handle_google_auth_request()

        # Handle Google callback with code
        elif path == "/auth/google/callback" and http_method == "POST":
            return handle_google_callback(event)

        # Handle preflight requests for CORS
        elif http_method == "OPTIONS":
            return generate_cors_response()

        # Default response for unknown paths
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"}),
            "headers": cors_headers(),
        }

    except Exception as e:
        # General error handling
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": cors_headers(),
        }


def handle_google_auth_request():
    """
    Generate the Google OAuth URL and return it.
    """
    redirect_uri = os.getenv("REDIRECT_URI")
    google_oauth_url = (
        f"{GOOGLE_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={os.getenv('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=openid%20email%20profile"
    )
    return {
        "statusCode": 200,
        "body": json.dumps({"redirect_url": google_oauth_url}),
        "headers": cors_headers(),
    }


def handle_google_callback(event):
    """
    Handle the callback from Google, exchange the code for a token, and fetch user info.
    """
    body = event.get("body")
    if not body:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Request body is empty or malformed"}),
            "headers": cors_headers(),
        }

    parsed_body = json.loads(body)
    code = parsed_body.get("code")
    if not code:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'code' is missing from the request body"}),
            "headers": cors_headers(),
        }

    try:
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
        token_response.raise_for_status()
        token_data = token_response.json()

        # Fetch user info
        user_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_response.raise_for_status()
        user_info = user_response.json()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Hi {user_info.get('name', 'Anonymous')}", "user": user_info}),
            "headers": cors_headers(),
        }

    except requests.exceptions.RequestException as e:
        # Handle HTTP errors from requests
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"HTTP error: {str(e)}"}),
            "headers": cors_headers(),
        }


def cors_headers():
    """
    Return CORS headers for all responses.
    """
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": os.getenv("FRONTEND_URL", "http://localhost:3003"),
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "OPTIONS, POST",
    }


def generate_cors_response():
    """
    Generate a CORS response for preflight requests.
    """
    return {
        "statusCode": 204,
        "body": "",
        "headers": cors_headers(),
    }
