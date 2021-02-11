import json

class User:
    def __init__(self, username, data=None):
        self.username = username
        if data:
            self.user_id = data.get('user_id')
            self.salary_day = data.get('salary_day')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'salary_day': self.salary_day
        }


def get_users():
    with open('database.json', 'r') as f:
        users = f.read()
        if users == '':
            return {}
        users = json.loads(users)
        return {
            username: User(username, user_data)
                for username, user_data in users.items()
        }


def save_users(users):
    users = {
        username: user.to_dict()
            for username, user in users.items()
    }
    with open('database.json', 'w') as f:
        f.writelines([json.dumps(users)])


def upsert_user_salary_date(username, user_id, day):
    users = get_users()
    if username not in users:
        users[username] = User(username)
    users[username].user_id = user_id
    users[username].salary_day = day
    save_users(users)
