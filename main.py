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


activity_template = """
{{app['name']}}: <{{html_url}}|{{title}}>\n{{summary}}
"""


DEFAULT_COLOR = "#808080"
COLORS = {
    "errorgroup": {"creat§ed": "bad"},
    "release": {"created": "good"},
}


def get_color(subject_type, action):
    return COLORS.get(subject_type, {}).get(action, DEFAULT_COLOR)

SLACK_URL = os.environ.get('SLACK_URL')
if not SLACK_URL:
    print("Missing environment variable SLACK_URL")
    exit(1)


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


@app.post('/new-activity')
def new_activity():
    data = request.json
    send(data)
    return "ok"


@app.get('/setup')
def setup():
    url = request.url.replace("/setup", "/new-activity")
    return template("This is your hook url, copy it:<h3>{{url}}</h3>", url=url)

if __name__ == '__main__':
    app.run()