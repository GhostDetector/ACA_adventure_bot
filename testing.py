import logging
import os
from csv import reader
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

print("Running")

#Random Joke Bot
@app.message(re.compile("^joke$"))  # type: ignore
def show_random_joke(message, say):
    """Send a random pyjoke back"""
    """
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    """
    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    logger.info(f"Sent joke < {joke} > to user {user_id}")
    l = joke.split('?')
    say(l[0]+ "?")
    say(l[1])
    #say(text=dm_channel + " " + joke, channel=dm_channel)

@app.event("app_mention")
def mention_handler(say):
    say("Commands are: [role, damage,dmg,class,job,pc, mob, monster, encounter]")


#Sees if a message is sent into chat reacts accordingly
@app.event("message")
def echo(message, say):
    print("Detected Message")
    msg = message["text"]
    s = msg.split(" ")
    
    #Roll regular roll with any number of dice
    if(s[0]=="roll"):
        dice = s[1].split("d")
        die = int(dice[0])
        result = int(dice[1])
        amt = []

        for x in range(die):
            ran = random.randrange(1,result)
            print("Rolling . . .  " + str(x))
            amt.append(str(ran))

        final = '-'.join(amt)
        say("Rolling:" + s[1] + " : [" + final + "]")

    #Rolls Damage dice
    if(s[0]=="Damage" or s[0]=="dmg"):
        print("damage")
        dice = s[1].split("d")
        die = int(dice[0])
        result = int(dice[1])
        amt = []
        total = 0
        for x in range(die):
            ran = random.randrange(1,result)
            print("Rolling . . .  " + str(x))
            amt.append(str(ran))
            total = total + ran

        final = '-'.join(amt)
        say("Rolling:" + s[1] + " : [" + final + "]\n " + "Damage: " + str(total))
    
    #Generates a random Class
    if(msg == "class" or msg == "Class" or msg == "job"):
        job = []
        with open("classes.csv", "r") as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for i in file_reader:
                job.append(i)
        r = random.randrange(0,len(job))
        tell = job[r]
        print (tell[0])
        say("Why not a " + tell[0] + "?")

    #Generates a Character + Class
    if(msg == "pc"):
        job = []
        with open("classes.csv", "r") as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for i in file_reader:
                job.append(i)
        race = []
        with open("races.csv", "r") as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for i in file_reader:
                race.append(i)
        r = random.randrange(0,len(race))
        b = random.randrange(0,len(job))
        ra = race[r]
        jo = job[b]
        print(race[r],job[b])
        say("Character: " +  ra[0] + " " + jo[0])

    #Generates a monster from monsterList.csv
    if(msg == "monster" or msg == "encounter" or msg == "mob"):
        mob = []
        with open("monsterList.csv", "r") as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for i in file_reader:
                mob.append(i)
        r = random.randrange(0,len(mob))
        tell = mob[r]
        print (tell[0])
        say("You encounter a " + tell[0] + "!")


if __name__=="__main__":
    #app.run(debug=True)
    handler = SocketModeHandler(app,slack_app_token)
    handler.start()
