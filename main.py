import json
import os
import requests
from flask import Flask
app = Flask(__name__)

from opbeat.contrib.flask import Opbeat

opbeat = Opbeat(
    app,
    organization_id = '8de432ce3f5742a29641d5f7430b9621',
    app_id = '8b0260935e',
    secret_token = '0a80dbc2d13fe4347e63411bb62839408249b1de'
)

class PrettySeriousError(Exception):
    pass


def send(data):
    rendered_activity = template(activity_template, **data)
    post_data = {
        "icon_url": "https://secure.gravatar.com/avatar/a6ec5537afa27bdb4fe5056e2d34810d",
        "username": "Opbeat",
        "attachments": [
            {
                "fallback": rendered_activity,
                "pretext": "{}: <{}|{}>".format(data['app']['name'], data['html_url'], data['title']),
                "color": get_color(data['subject_type'], data['action']),
                "fields": [
                    {
                        "value": data['summary'],
                        "short": False
                    }
                ]
            }
        ]
    }

    resp = requests.post(
        SLACK_URL,
        data={"payload": json.dumps(post_data)}
    )
    if resp.status_code != 200:
        print(resp.status_code, resp.text)
    else:
        print("Sent activity to slack")


@app.route('/new-activity')
def new_activity():
    raise PrettySeriousError("Show them the app, Ron")
    return "ok"

if __name__ == '__main__':
    app.run()