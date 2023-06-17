import logging
import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Slack Token
TOKEN = ''

client = WebClient(token=TOKEN, ssl=ctx)
logger = logging.getLogger(__name__)

api_response = client.api_test()

print(api_response)

# Channel on which to send message to
channel_id = "U02JQF18GJV"

if __name__ == '__main__':
    try:
        result = client.chat_postMessage(channel=channel_id, text="Hello from python")
        print(result)
    except SlackApiError as e:
        print(f"Error: {e}")
