import json

def _read_data():
    with open('database.json', 'w+') as f:
        data = f.read()
        if data == '':
            return {}
        return json.loads(data)


def _write_data(data):
    with open('database.json', 'w') as f:
        f.writelines([json.dumps(data)])


def upsert_user_salary_date(user, day):
    data = _read_data()
    if user not in data:
        data[user] = {}
    data[user]['salary_day'] = day
    _write_data(data)
