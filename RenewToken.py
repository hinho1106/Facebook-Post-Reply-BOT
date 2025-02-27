import boto3
import requests
import json
import os

# AWS Secrets Manager Client
secrets_client = boto3.client('secretsmanager')

# Facebook App Credentials
APP_ID = "APP_ID"
APP_SECRET = "APP_SECRET"
FB_PAGE_ID = "FB_PAGE_ID"
SECRET_NAME = "facebook/api/access-token"  # AWS Secrets Manager Key Name

def get_secret():
    """Retrieve the existing Facebook token from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(response['SecretString'])
        return secret.get("LONG_LIVED_USER_ACCESS_TOKEN")
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

def update_secret(user_token, page_token):
    """Update the token in AWS Secrets Manager."""
    #status: 1:user, 2:page
    try:
        secrets_client.put_secret_value(
            SecretId=SECRET_NAME,
            SecretString=json.dumps({"LONG_LIVED_USER_ACCESS_TOKEN": user_token, "LONG_LIVED_PAGE_ACCESS_TOKEN": page_token})
        )
        
        print("Successfully updated the page and user access token in AWS Secrets Manager.")
        
    except Exception as e:
        print(f"Error updating secret: {e}")

def refresh_access_token():
    """Refresh the long-lived user access token and update the stored secret."""
    current_token = get_secret()
    if not current_token:
        print("No current token found.")
        return None

    # Step 1: Exchange for a new long-lived user token
    refresh_url = f"https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={current_token}"
    
    response = requests.get(refresh_url)
    print(response.json())

    if response.status_code == 200:
        new_user_token = response.json().get("access_token")
        # update_secret(new_user_token, 1)

        # Step 2: Fetch a new page access token
        page_token_url = f"https://graph.facebook.com/v22.0/me/accounts?access_token={new_user_token}"
        page_response = requests.get(page_token_url)

        print(page_response.json())
        # print(page_response.status_code)

        if page_response.status_code == 200:
            pages = page_response.json().get("data", [])
            for page in pages:
                new_page_token = page.get("access_token")
                print(new_page_token)
                update_secret(new_user_token, new_page_token)
                return new_page_token
        else:
            print("Failed to fetch page access token.")
            return None
    else:
        print("Failed to refresh access token.")
        return None


def lambda_handler(event, context):
    print("Hello")
    new_token = refresh_access_token()
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Token refreshed", "new_token": new_token})
    }
