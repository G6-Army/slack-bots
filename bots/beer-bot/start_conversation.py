"""
This script should run once a day to start a conversation with people
who will get salary in the upcoming days.
"""
import db
from slack import app

# TODO: read from db who has upcoming salary
# here is how to start conversation - U01MXA4CK9P is user id
# app.client.chat_postMessage(channel='U01MXA4CK9P', text='test')
