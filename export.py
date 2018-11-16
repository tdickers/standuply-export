# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import os
import pprint
import time
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

# Uncomment to find your channel ID
# channels = sc.api_call("channels.list")
# for channel in channels['channels']:
#     print channel['name']
#     print channel['id']
channel_id = '<fill in your own>'
start_ts = '<fill in your own>'

def format_report(message):
    ts = time.gmtime(int(float(message['ts'])))
    time_printed = False
    fields = message['attachments'][0]['fields']
    for field in fields:
        if field['title'] == 'No answers':
            break
        if not time_printed:
            print '> ' + time.strftime('%b %d', ts) + ':'
            time_printed = True
        print u'Q: ' + field['title']
        print u'A: ' + field['value']
        print

def messages_since(ts):
    channel_history = sc.api_call("channels.history", channel=channel_id, oldest=ts)
    return channel_history

while True:
    old_start_ts = start_ts
    messages = messages_since(start_ts)

    if not messages['ok']:
        print 'bad response'
        print messages
        exit(1)

    for message in reversed(messages['messages']):
        if 'username' in message and message['username'] == '<fill in your own>' and 'attachments' in message:
            format_report(message)

        if float(message['ts']) > float(start_ts):
            start_ts = message['ts']

    if old_start_ts == start_ts:
        exit(0)

    time.sleep(1)
