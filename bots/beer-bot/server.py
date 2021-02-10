"""
The server is reacting to events from users interacting with the bot.
"""
import db
from slack import app

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Да треперят",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Да",
                            "emoji": True
                        },
                        "value": "yes",
                        "action_id": "yes"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Не",
                            "emoji": True
                        },
                        "value": "no",
                        "action_id": "no"
                    }
                ]
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("yes")
def yes(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked yes")


@app.action("no")
def yes(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked no")


@app.command("/register")
def register(ack, say, command):
    # Acknowledge command request
    ack()
    user = command['user_name']
    raw_day = command['text']
    try:
        day = int(raw_day)
        if day < 1 or day > 31:
            raise ValueError()

        db.upsert_user_salary_date(user, day)

        say(f"<@{user}> взима заплата на {day} число")
    except ValueError:
        say(f"<@{user}> въведе невалидно число на заплата {raw_day}")


# Start your app
if __name__ == "__main__":
    app.start(port=6666)
