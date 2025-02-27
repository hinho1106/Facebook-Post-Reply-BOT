import boto3
import requests
import json
import os

## AWS Secrets Manager Client
secrets_client = boto3.client('secretsmanager')

## Facebook Page Post Global Variables
FACEBOOK_PAGE_POST_ID = "1234567890_012345667"
FACEBOOK_PAGE_ID = 1234567890
GRAPH_API_VERSION = "v22.0"
URL_PREFIX = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
PAGE_LIMIT = 5000

## Reply/Comment Message Global Variables
REPLY_MESSAGE = "Thank you for your message. We will get back to you as soon as possible."
COMMENT_MESSAGE = "Thank you for your comment. We will get back to you as soon as possible."

## AWS Secrets Manager Key Name
SECRET_NAME = "facebook/api/access-token"  


def GetPageAccessToken():
    """Retrieve the existing Facebook token from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(response['SecretString'])
        return secret.get("LONG_LIVED_PAGE_ACCESS_TOKEN")
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None


def GetPagePostComments(page_token):
    url = f"{URL_PREFIX}/{FACEBOOK_PAGE_POST_ID}/comments?access_token={page_token}"
    response = requests.get(url)
    if response.status_code == 200:
        page_post_comments = response.json()
        # print("Page Post Comments:", page_post_comments)
        ReplyMessageToUsers(page_post_comments, page_token)  
    else:
        print(f"Failed to retrieve Page Post Comments. Status code: {response.status_code}")

def HasSubComments(comment_id, page_token):
    url = f"{URL_PREFIX}/{comment_id}/comments?access_token={page_token}"
    response = requests.get(url)
    if response.status_code == 200:
        comments = response.json()
        if(comments.get("data", [])):
            return True
        else:
            return False
    else:
        print(f"Failed to retrieve User Comments. Status code: {response.status_code}")
        return None

def MessageToUser(comment_id, page_token):
    url = f"{URL_PREFIX}/{FACEBOOK_PAGE_ID}/messages?access_token={page_token}&limit={PAGE_LIMIT}"
    data = {
        "recipient": {"comment_id": comment_id},
        "message": {"text": REPLY_MESSAGE},
        "messaging_type": "RESPONSE"
    }
    headers = {'content-type':  'application/json'}
    # print(json.dumps(data))
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Failed to reply to user. Status code: {response.status_code}")
        print(response.text)

def CommentToUser(comment_id, page_token):
    url = f"{URL_PREFIX}/{comment_id}/comments?access_token={page_token}"
    data = {
        "message": COMMENT_MESSAGE
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to comment to user. Status code: {response.status_code}")

def ReplyMessageToUsers(post_comments, page_token):
    # print(post_comments)
    comments = post_comments.get("data", [])
    # print(comments)
    for comment in comments:
        comment_id = comment.get("id")
        # print(comment_id)
        if not HasSubComments(comment_id, page_token):
            MessageToUser(comment_id, page_token)
            CommentToUser(comment_id, page_token)
            
           
def lambda_handler(event, context):
    ## Get Page Access Token
    page_token = GetPageAccessToken()
    if page_token:
        # print("Page Access Token:", page_token)
        ## Get Page Post Comments
        GetPagePostComments(page_token)
    else:
        print("Failed to retrieve Page Access Token.")
    
