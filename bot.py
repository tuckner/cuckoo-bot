#!/usr/bin/env python

import os
import time
import re
import requests
import json
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('slack'))
api = os.environ.get('cuckoo')

starterbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format("help")

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    if command.startswith("submit"):
        hash = command.replace('submit ', '', 1)
        if str(len(hash)) in ["32", "40", "64"]:
            data = {"strings": hash.encode('utf8'), "timeout": 60}
            resp = requests.post(api + '/tasks/create/submit', headers=headers, data=data) 
            try:
                resp_content = json.loads(resp.content)
                response = "Thanks for submitting! Your task ID is: {}".format(resp_content['task_ids'][0])
            except Exception as e:
                response = "No task ID returned, either the hash is not in VT or an error occurred"
                print(e)
        else:
            response = "Please submit a valid hash"
    elif command.startswith("status"):
        id = command.replace('status ', '', 1)
        resp = requests.get(api + '/tasks/view/{}'.format(id), headers=headers)
        try:
            resp_content = resp.json()
            response = '''
            Task Added on: {}\nTask Completed on: {}
            '''.format(resp_content['task']['added_on'], resp_content['task']['completed_on'])
        except:
            response = "An error occurred looking up the task id"
    elif command.startswith("health"):
        resp = requests.get(api + '/cuckoo/status/', headers=headers)
        try:
            resp_content = resp.json()
            if resp_content.get('message') == "Internal server error":
                response = "API is down"
            else:
                response = "API is working"
        except:
            response = "An error occurred getting current health"
    elif command.startswith("score"):
        id = command.replace('score ', '', 1)
        resp = requests.get(api + '/tasks/report/{}'.format(id), headers=headers)
        try:
            resp_content = resp.json()
            if resp_content.get('signatures'):
                resp_add = ''
                for signature in resp_content.get('signatures'):
                    resp_add += '- {}\n'.format(signature['description'])
                response = '''
                The score for task *{}* is `{}`. Signatures matched include:\n{} 
                '''.format(id, resp_content['info']['score'], resp_add)
            else:
                response = '''
                The score for task *{}* is `{}`. There were no signatures detections. Try working with an analyst to manually interact with this submission.
                '''.format(id, resp_content['info']['score'])

        except Exception as e:
            print(e)
            response = "An error occurred looking up the task id"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        attachments=attachments
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
