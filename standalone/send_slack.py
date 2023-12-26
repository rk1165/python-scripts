import logging
import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Slack Token
TOKEN = ''
# Channel ID of the channel on which to send message to
CHANNEL_ID = ""

client = WebClient(token=TOKEN, ssl=ctx)
logger = logging.getLogger(__name__)

api_response = client.api_test()

print(api_response)

if __name__ == '__main__':
    try:
        result = client.chat_postMessage(channel=CHANNEL_ID, text="Hello from python")
        print(result)
    except SlackApiError as e:
        print(f"Error: {e}")
