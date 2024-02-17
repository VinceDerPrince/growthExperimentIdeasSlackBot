#!/usr/bin/env python3

import slack
from flask import Flask, request, jsonify
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import json

load_dotenv()  # take environment variables from .env.
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = slack.WebClient(token=SLACK_TOKEN)

@app.route('/slack/idea', methods=['POST'])
def handle_slash_command():
    # Parse the request payload
    data = request.form
    print(data)
    trigger_id = data.get('trigger_id')

    # Define a simple modal
    modal = {
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "My App",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "experiment_name",
			"element": {
				"type": "plain_text_input",
				"action_id": "name",
				"placeholder": {
					"type": "plain_text",
					"text": "Geben Sie den Namen des Experiments ein"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Name des Experiments"
			}
		},
		{
			"type": "input",
			"block_id": "hypothesis",
			"element": {
				"type": "plain_text_input",
				"action_id": "hypo_input",
				"multiline": True,
				"placeholder": {
					"type": "plain_text",
					"text": "Welche Hypothese testen Sie?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Hypothese"
			}
		},
		{
			"type": "input",
			"block_id": "expected_impact",
			"element": {
				"type": "plain_text_input",
				"action_id": "impact_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Welchen Effekt erwarten Sie?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Erwarteter Effekt"
			}
		},
		{
			"type": "input",
			"block_id": "measurement_method",
			"element": {
				"type": "plain_text_input",
				"action_id": "measure_input",
				"multiline": True,
				"placeholder": {
					"type": "plain_text",
					"text": "Wie werden die Ergebnisse gemessen?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Messmethode"
			}
		},
		{
			"type": "input",
			"block_id": "additional_details",
			"element": {
				"type": "plain_text_input",
				"action_id": "details_input",
				"multiline": True,
				"placeholder": {
					"type": "plain_text",
					"text": "Gibt es weitere Details oder benötigte Ressourcen?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Weitere Details"
			}
		}
	]
}
    
    # Open the modal
    client.views_open(trigger_id=trigger_id, view=modal)
    return '', 200

@app.route('/slack/interactive', methods=['POST'])
def handle_interactive():
    payload = request.form.to_dict()
    response_payload = json.loads(payload.get('payload'))

    # Assuming this endpoint handles the modal submission
    if response_payload["type"] == "view_submission":
        # Extract the values submitted by the user
        user = response_payload['user']['id']
        values = response_payload['view']['state']['values']
        experiment_name = values['experiment_name']['name']['value']
        hypothesis = values['hypothesis']['hypo_input']['value']
        expected_impact = values['expected_impact']['impact_input']['value']
        measurement_method = values['measurement_method']['measure_input']['value']
        additional_details = values['additional_details']['details_input']['value']

        # Construct the message block to post to a channel
        message_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Submitted by: <@{user}>"
                }
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Experiment Name:* {experiment_name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hypothesis:* {hypothesis}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Expected Impact:* {expected_impact}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Measurement Method:* {measurement_method}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Additional Details:* {additional_details}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🚀 *Beteiligt euch am Experiment!* 🚀\nStimmt über das Experiment ab durch Reagieren mit 👍 und 👎. Oder diskutiert das Experiment ausführlich im Thread zu dieser Submission. Eure Meinungen und Ideen sind wichtig, um gemeinsam zu wachsen!"
                }
            }
        ]

        # Post the message to a specific channel
        client.chat_postMessage(channel='#experiments', blocks=message_blocks)
        return '', 200

if __name__ == "__main__":
    app.run(debug=True)
    #ngrok http --domain=visually-dominant-swift.ngrok-free.app 5000
