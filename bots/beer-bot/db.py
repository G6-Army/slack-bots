import json

class User:
    def __init__(self, user_id, data={}):
        self.user_id = user_id
        self.username = data.get('username')
        self.salary_day = data.get('salary_day')
        self.flex_status = data.get('flex_status')
        self.location_of_flex = data.get('location_of_flex')
        self.time_of_flex = data.get('time_of_flex')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'salary_day': self.salary_day,
            'flex_status': self.flex_status,
            'location_of_flex': self.location_of_flex,
            'time_of_flex': self.time_of_flex,
            'username': self.username
        }


def get_users():
    with open('database.json', 'r') as f:
        users = f.read()
        if users == '':
            return {}
        users = json.loads(users)
        return {
            user_id: User(user_id, user_data)
                for user_id, user_data in users.items()
        }


def save_users(users):
    users = {
        user_id: user.to_dict()
            for user_id, user in users.items()
    }
    with open('database.json', 'w') as f:
        f.writelines([json.dumps(users)])


def upsert_user_data(user_id, **kwargs):
    users = get_users()
    if user_id not in users:
        users[user_id] = User(user_id)
    for key, val in kwargs.items():
        setattr(users[user_id], key, val)
    save_users(users)


def get_user_by_id(user_id):
    return get_users().get(user_id)
