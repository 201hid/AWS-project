import json
import requests
from aws_lambda_powertools.utilities.typing import LambdaContext

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Hardcoded values
HARDCODED_CLIENT_ID = "128876871494-ddangphp27biloi2uoikvr9o21bhgrll.apps.googleusercontent.com"
HARDCODED_CLIENT_SECRET = "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"
HARDCODED_REDIRECT_URI = "https://q01x8trvnb.execute-api.us-east-1.amazonaws.com/Prod/auth/google/callback"
HARDCODED_FRONTEND_URL = "http://localhost:3003"

def lambda_handler(event, context: LambdaContext):
    try:
        # Log incoming event for debugging
        print("Incoming event:", json.dumps(event))

        path = event.get("path")
        http_method = event.get("httpMethod")

        # Handle OAuth redirection request
        if path == "/auth/google" and http_method == "POST":
            return handle_google_auth_request()

        # Handle Google callback with GET (preferred for callback URLs)
        elif path == "/auth/google/callback" and http_method == "GET":
            return handle_google_callback_get(event)

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
        print("Unhandled exception:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
            "headers": cors_headers(),
        }


def handle_google_auth_request():
    """
    Generate the Google OAuth URL and return it.
    """
    try:
        google_oauth_url = (
            f"{GOOGLE_AUTH_URL}"
            f"?response_type=code"
            f"&client_id={HARDCODED_CLIENT_ID}"
            f"&redirect_uri={HARDCODED_REDIRECT_URI}"
            f"&scope=openid%20email%20profile"
        )
        print("Generated Google OAuth URL:", google_oauth_url)
        return {
            "statusCode": 200,
            "body": json.dumps({"redirect_url": google_oauth_url}),
            "headers": cors_headers(),
        }
    except Exception as e:
        print("Error generating Google OAuth URL:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to generate Google OAuth URL"}),
            "headers": cors_headers(),
        }


def handle_google_callback_get(event):
    """
    Handle the callback from Google for GET requests, exchange the code for a token, and fetch user info.
    """
    query_params = event.get("queryStringParameters", {})
    print("Query parameters:", query_params)  # Log query parameters for debugging

    code = query_params.get("code")
    print("Received authorization code:", code)  # Log received code

    if not code:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'code' is missing from the query parameters"}),
            "headers": cors_headers(),
        }

    try:
        # Exchange code for access token
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": HARDCODED_CLIENT_ID,
                "client_secret": HARDCODED_CLIENT_SECRET,
                "redirect_uri": HARDCODED_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        token_data = token_response.json()
        print("Token response:", token_data)

        if "access_token" not in token_data:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Access token missing in response"}),
                "headers": cors_headers(),
            }

        # Fetch user info
        user_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_response.raise_for_status()
        user_info = user_response.json()
        print("User info:", user_info)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Hi {user_info.get('name', 'Anonymous')}", "user": user_info}),
            "headers": cors_headers(),
        }

    except requests.exceptions.RequestException as e:
        print("Error during callback handling:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve data from Google APIs", "details": str(e)}),
            "headers": cors_headers(),
        }


def cors_headers():
    """
    Return CORS headers for all responses.
    """
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": HARDCODED_FRONTEND_URL,
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
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
