"""
This script should run once a day to start a conversation with people
who will get salary in the upcoming days.
"""
from datetime import date, timedelta

import db
from slack import app


print('Checking for upcoming salaries')

today = date.today()
one_day = timedelta(days=1)
next_five_days = set((today + i * one_day).day for i in range(1, 6))
for user in db.get_users().values():
    if user.salary_day in next_five_days:
        print(f'User {user.username} has an upcoming salary')
        # TODO: start meaningful conversation
        app.client.chat_postMessage(channel=user.user_id, text='test')

print('Done checking for upcoming salaries')
