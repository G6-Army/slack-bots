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


@app.action("yes1")
@app.action("yes2")
@app.action("yes3")
def yes(body, ack, say):
    # Acknowledge the action
    ack()

    user_id = body['user']['id']
    db.upsert_user_data(user_id, flex_status='yes')

    say(blocks=[
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Къде?",
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
                        "text": "Вкъщи",
                        "emoji": True
                    },
                    "action_id": "home",
                    "style": "primary"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "В барче",
                        "emoji": True
                    },
                    "action_id": "bar",
                    "style": "primary"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "В паркче",
                        "emoji": True
                    },
                    "action_id": "park",
                    "style": "primary"
                }
            ]
        }
    ])


@app.action("no")
def no(body, ack, say):
    # Acknowledge the action
    ack()

    user_id = body['user']['id']
    db.upsert_user_data(user_id, flex_status='no')

    say(f"Жалко...")

@app.action("home")
def home(body, ack, say):
    ack()
    location('вкъщи', body, say)

@app.action("bar")
def bar(body, ack, say):
    ack()
    location('в барче', body, say)

@app.action("park")
def park(body, ack, say):
    ack()
    location('в паркче', body, say)

def location(loc, body, say):
    user_id = body['user']['id']
    db.upsert_user_data(user_id, location_of_flex=loc)
    say(blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "В колко"
            },
            "accessory": {
                "type": "timepicker",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select time",
                    "emoji": True
                },
                "action_id": "time"
            }
        }
    ])

@app.action("time")
def time(body, ack, say):
    ack()
    user_id = body['user']['id']
    selected_time = body['actions'][0]['selected_time']
    db.upsert_user_data(user_id, time_of_flex=selected_time)
    user = db.get_user_by_id(user_id)
    app.client.chat_postMessage(channel='C01KHB3H77Z', text=f"Утре в {selected_time} <@{user_id}> ще черпи {user.location_of_flex}")

@app.command("/register")
def register(ack, say, command):
    # Acknowledge command request
    ack()
    username = command['user_name']
    user_id = command['user_id']
    raw_day = command['text']
    try:
        day = int(raw_day)
        if day < 1 or day > 31:
            raise ValueError()

        db.upsert_user_data(user_id, username=username, salary_day=day)

        say(f"<@{username}> взима заплата на {day} число")
    except ValueError:
        say(f"<@{username}> въведе невалидно число на заплата {raw_day}")


# Start your app
if __name__ == "__main__":
    app.start(port=6666)
