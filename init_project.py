import os

TEMPLATE_YAML = """
Globals:
  Function:
    Runtime: python3.9
    Timeout: 30
    MemorySize: 128

Resources:
  AuthFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      CodeUri: src/lambda
      Environment:
        Variables:
          GOOGLE_CLIENT_ID: !Ref GoogleClientId
          GOOGLE_CLIENT_SECRET: !Ref GoogleClientSecret
          REDIRECT_URI: "http://localhost:3003"  # Update for production
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /auth/google
            Method: POST

Parameters:
  GoogleClientId:
    Type: String
    Description: Google OAuth Client ID
  GoogleClientSecret:
    Type: String
    Description: Google OAuth Client Secret
"""

LAMBDA_CODE = """
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
"""

def create_directory_structure():
    os.makedirs("src/lambda", exist_ok=True)
    with open("template.yaml", "w") as f:
        f.write(TEMPLATE_YAML.strip())
    with open("src/lambda/app.py", "w") as f:
        f.write(LAMBDA_CODE.strip())

def main():
    print("Initializing project structure...")
    create_directory_structure()
    print("Project initialized!")
    print("Next steps:")
    print("1. Update `template.yaml` with your Google OAuth Client ID and Secret.")
    print("2. Install dependencies in `src/lambda` by running:")
    print("     pip install requests aws-lambda-powertools -t src/lambda")
    print("3. Build and deploy with SAM:")
    print("     sam build && sam deploy --guided")

if __name__ == "__main__":
    main()
