"""
This script should run once a day to keep user invite data up to date
"""
from datetime import date, timedelta

import db

print('Cleaning up invite data')

today = date.today()
one_day = timedelta(days=1)
last_five_days = {(today - i * one_day).day for i in range(1, 6)}

users = db.get_users()
for user in users.values():
    if (user.invitation_status == 'yes' and user.invite_day in last_five_days) or \
            (user.invitation_status == 'no' and user.salary_day in last_five_days):
        print(f'Cleaning up {user.username} invitation')
        user.invite_day = None
        user.invitation_status = None
db.save_users(users)

print('Done cleaning up invite data')
