'''
This script should run once a day to start a conversation with people
who will get salary in the upcoming days.

Also keeps user invite data up to date.
'''
from datetime import date, timedelta

import db
from slack import app


print('Checking for upcoming salaries')

today = date.today()
one_day = timedelta(days=1)
next_five_days = {(today + i * one_day).day for i in range(1, 6)}
for user in db.get_users().values():
    if user.flex_status is None and user.salary_day in next_five_days:
        print(f'User {user.username} has an upcoming salary')
        app.client.chat_postMessage(channel=user.user_id, text='ще черпиш ли утре', blocks=[
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': 'Смяташ ли да флексваш утре, маняченце?',
                    'emoji': True
                }
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'MN QSNOOOOO !!!1!',
                            'emoji': True
                        },
                        'value': 'yes',
                        'action_id': 'yes1',
                        'style': 'primary'
                    },
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Че как',
                            'emoji': True
                        },
                        'value': 'yes',
                        'action_id': 'yes2',
                        'style': 'primary'
                    },
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Иска ли питане',
                            'emoji': True
                        },
                        'value': 'yes',
                        'action_id': 'yes3',
                        'style': 'primary'
                    },
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Не',
                            'emoji': True
                        },
                        'value': 'no',
                        'action_id': 'no',
                        'style': 'danger'
                    }
                ]
            }
	])

print('Done checking for upcoming salaries')

print('Cleaning up invite data')

today = date.today()
one_day = timedelta(days=1)
last_five_days = {(today - i * one_day).day for i in range(1, 6)}

users = db.get_users()
for user in users.values():
    if user.salary_day in last_five_days:
        print(f'Cleaning up {user.username} invitation')
        user.flex_status = None
        user.location_of_flex = None
        user.time_of_flex = None
db.save_users(users)

print('Done cleaning up invite data')
