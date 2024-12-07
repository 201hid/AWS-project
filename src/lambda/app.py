import json
import requests
from aws_lambda_powertools.utilities.typing import LambdaContext
from jose import jwt, JWTError
import os

# Environment variables
USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
REGION = os.getenv("REGION")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")

COGNITO_ISSUER = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

# Cached JWKS keys
JWKS = None


def lambda_handler(event, context: LambdaContext):
    try:
        # Log the incoming event
        print("Incoming event:", json.dumps(event))

        path = event.get("path")
        http_method = event.get("httpMethod")

        # Handle Google OAuth request
        if path == "/auth/google" and http_method == "GET":
            return handle_google_auth_request()

        # Handle Google OAuth callback
        elif path == "/auth/google/callback" and http_method == "GET":
            return handle_google_callback(event)

        # Default response for unknown paths
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"}),
            "headers": cors_headers(),
        }

    except Exception as e:
        print("Unhandled exception:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
            "headers": cors_headers(),
        }


def handle_google_auth_request():
    """
    Generate the Cognito-hosted Google OAuth URL.
    """
    cognito_oauth_url = (
        f"{COGNITO_ISSUER}/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=email+openid+profile"
    )
    print("Generated Cognito OAuth URL:", cognito_oauth_url)
    return {
        "statusCode": 200,
        "body": json.dumps({"redirect_url": cognito_oauth_url}),
        "headers": cors_headers(),
    }


def handle_google_callback(event):
    """
    Validate the Cognito token and fetch user info.
    """
    query_params = event.get("queryStringParameters")
    if not query_params or "code" not in query_params:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Authorization code is missing"}),
            "headers": cors_headers(),
        }

    code = query_params["code"]
    print("Authorization code:", code)

    try:
        # Exchange authorization code for tokens
        token_response = requests.post(
            f"{COGNITO_ISSUER}/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        print("Token response:", tokens)

        id_token = tokens.get("id_token")
        if not id_token:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "ID token is missing in response"}),
                "headers": cors_headers(),
            }

        # Validate the ID token
        user_info = validate_cognito_token(id_token)
        if not user_info:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Invalid token"}),
                "headers": cors_headers(),
            }

        print("User info:", user_info)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Hi {user_info.get('email', 'User')}", "user": user_info}),
            "headers": cors_headers(),
        }

    except requests.exceptions.RequestException as e:
        print("Error during token exchange:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Token exchange failed", "details": str(e)}),
            "headers": cors_headers(),
        }


def validate_cognito_token(token):
    """
    Validate the ID token using Cognito's JWKS.
    """
    global JWKS
    if not JWKS:
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        JWKS = response.json()

    try:
        # Decode and validate the JWT
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        key = next(k for k in JWKS["keys"] if k["kid"] == kid)

        decoded_token = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=COGNITO_ISSUER,
        )
        return decoded_token
    except JWTError as e:
        print("Token validation failed:", str(e))
        return None


def cors_headers():
    """
    Return CORS headers for all responses.
    """
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": FRONTEND_URL,
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "OPTIONS, GET, POST",
    }
