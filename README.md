# Growth Experiment Idea Submission Bot for Slack

## Overview

The Growth Experiment Idea Submission Bot is a Slack application designed to facilitate the submission and discussion of growth experiment ideas within organizations. Inspired by the principles outlined in "Hacking Growth" by Sean Ellis, this bot provides a structured way for teams to propose, review, and collaborate on growth experiments directly within Slack. 

## Features

- **Modal Submission Form**: Users can submit their experiment ideas through a custom Slack modal, which includes fields for the experiment's name, hypothesis, expected impact, method of measurement, and additional details.

- **Automated Idea Posting**: Once a form is submitted, the bot automatically posts the idea to a specified Slack channel, encouraging team-wide discussion and collaboration.

- **User Mentioning**: The submission includes an @mention of the user who submitted the idea, facilitating easy recognition and direct feedback.

- **Interactive Voting**: The bot's post encourages team members to vote on the idea using emoji reactions and to discuss the idea further in a dedicated thread.

## Setup

### Prerequisites

- A Slack account with permissions to create apps.
- Python 3.x and pip installed on your server.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/VinceDerPrince/growthExperimentIdeasSlackBot.git
   cd growthExperimentIdeasSlackBot
   ```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
3. **Configure Environment Variables**
Create a .env file in the root directory of the project and add your Slack Bot Token and Signing Secret:
```bash
SLACK_TOKEN=your_slack_bot_token_here
SIGNING_SECRET=your_slack_signing_secret_here
```
4. **Start the Flask Application**
```bash
python src/bot.py
```

## Slack App Configuration
1. **Create a New Slack App** in your workspace via the Slack API website.
2. Add OAuth Scopes for `commands`, `chat:write`, and `chat:write.public`.
3. **Enable Interactivity & Shortcuts** and set the request URL to your server where the Flask app is running.
4. **Create a Slash Command** (e.g., `/submit-idea`) and set the request URL accordingly.
5. **Install the App** to your workspace.

## Usage
- Type `/submit-idea` in any channel or direct message to open the idea submission modal.
- Fill in the form with your experiment idea and submit.
- The bot will post the submission to the configured channel for team review and discussion.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.