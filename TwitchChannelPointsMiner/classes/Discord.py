from textwrap import dedent

import requests
import json
from TwitchChannelPointsMiner.classes.Settings import Events

class Discord(object):
    __slots__ = ["webhook_api", "events"]

    def __init__(self, webhook_api: str, events: list):
        self.webhook_api = webhook_api
        self.events = [str(e) for e in events]

    def send(self, message: str, event: Events, record) -> None:
        if str(event) in self.events:
            if record.is_online is True:
                status = "Online"
                color = "65280"
            else:
                status = "Offline"
                color = "16711680"
            embed = {
                "title": "Twitch Channel Points Miner",
                "url": record.streamer_url,
                "color": color,
                "fields": [
                    {
                        "name": "Username",
                        "value": dedent(f"{record.username}")
                    },
                    {
                        "name": "Channel Points",
                        "value": dedent(f"{record.channel_points}")
                    }
                ]
            }
            data = {
                'username': 'Twitch Channel Points Miner',
                'avatar_url': 'https://i.imgur.com/X9fEkhT.png',
                'content': dedent(f"<@&738009117519511652>\nStreamer `{record.username}` is {status}!\nPoints Earned: {record.channel_points}"),
                'embeds': [embed]
            }
            payload = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.webhook_api, data=payload, headers=headers)
            if response.status_code == 204:
                print("Message with embed sent successfully")
            else:
                print(f"Failed to send message with embed. Status code: {response.status_code}")
                print(response.text)
