import logging
import os
import pandas as pd
import random
import re

from dotenv import load_dotenv
import pyjokes
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)

load_dotenv()

slack_app_token = os.environ["apptoken"]
slack_bot_token = os.environ["bottoken"]

app = App(token=slack_bot_token)
logger = logging.getLogger(__name__)

channel_name = "bot-testing"

print("Running")
job = ["Barbarian", "Cleric", "Rogue", "Druid", "Ranger", "Paladin", "Fighter"]

@app.message(re.compile("^joke$"))  # type: ignore
def show_random_joke(message, say):
    """Send a random pyjoke back"""
    channel_type = message["channel_type"]
    if channel_type != "im":
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    logger.info(f"Sent joke < {joke} > to user {user_id}")

    say(text=joke, channel=dm_channel)

@app.message(re.compile("^joke$"))
def show_joke(message,say):
    print("sent msg")
    channel_type = message ["channel_type"]
    dm_channel= message['channel']
    user_id = message["user"]
    say("No")

@app.event("app_mention")
def mention_handler(say):
    print("Talk")
    say("Whats Up")

@app.event("message")
def echo(message, say):
    print("Detected Message")
    msg = message["text"]
    s = msg.split(" ")
    
    if(s[0]=="roll"):
        print("roll")
        s = s[1].split("d")
        die = int(s[0])
        result = int(s[1])
        amt = []

        for x in range(die):
            ran = random.randrange(1,result)
            amt.append(str(ran))

        final = '-'.join(amt)
        say("Roll [" + final + "]")

    if(s[0]=="Damage" or s[0]=="dmg"):
        print("damage")
        s = s[1].split("d")
        die = int(s[0])
        result = int(s[1])
        amt = []
        total = 0
        for x in range(die):
            ran = random.randrange(1,result)
            amt.append(str(ran))
            total = total + ran

        final = '-'.join(amt)
        say("Roll [" + final + "]\n " + "Damage: " + str(total))
    if(msg == "class" or msg == "Class"):
        data = pd.read_csv('classes.csv')
        data.head()
        r = random.randrange(0,len(job))
        say(job[r])


if __name__=="__main__":
    #app.run(debug=True)
    handler = SocketModeHandler(app,slack_app_token)
    handler.start()
