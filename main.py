import os
import discord  #importing the library
import requests  #to make HTTP requests
import json  #to make JSON requests
import random  #to select messages randomly.
from replit import db  #to use the replit db
from serpapi import GoogleSearch

my_secret = os.environ['Token']
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)

sad_words = [
    'sad', 'depressed', 'stressed', 'unhappy', 'angry', 'miserable',
    'depressing', 'stressing', 'rude'
]

encouragements = [
    "Cheer up!", "Hang in there.", "You are a great soul!",
    "Great days will come."
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quotes():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_input):
    if "encouragements" in db.keys():
        encourage = db["encouragements"]
        encourage.append(encouraging_input)
        db["encouragements"] = encourage
    else:
        db["encouragements"] = [encouraging_input]


def delete_message(index):
    encourage = db["encouragements"]
    if len(encourage) > index:
        del encourage[index]
        db["encouragements"] = encourage

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user: return

    if msg.startswith(('hello', 'hi', 'Hello', 'Hello!', 'hey')):
        await message.channel.send('Hello!')

    if msg.startswith('$inspire'):
        quote = get_quotes()
        await message.channel.send(quote)

    if db["responding"]:
        options = encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_input = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_input)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encourage = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_message(index)
            encourage = db["encouragements"].value
        await message.channel.send(encourage)

    if msg.startswith("$list"):
        encourage = []
        if "encouragements" in db.keys():
            encourage = db["encouragements"].value
        await message.channel.send(encourage)

    if msg.startswith("$responding"):
        val = msg.split("$responding ", 1)[1]

        if val.lower() == "on":
            db["responding"] = True
            await message.channel.send("Responding is ON.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is OFF.")

    if msg.startswith("$show"):
        val = msg.split("$show", 1)[1]

        my_secret = os.environ['API key']
        params = {
            "api_key": my_secret,
            "engine": "google",
            "q": val,
            "hl": "en",
            "tbm": "isch"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        image_results = []

        for image in results["images_results"]:
            image_results.append({"original": image["original"]})

        for j in range(1, 7):
            await message.channel.send(image_results[j]["original"])
        await message.channel.send(
            "Here you go.\nHave any more questions:question:\nFeel free to ask again :smiley: !"
        )

    if msg.startswith("$find"):
        val = msg.split("$find", 1)[1]

        my_secret = os.environ['API key']
        params = {
            "api_key": my_secret,
            "engine": "google",
            "q": val,
            "hl": "en"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        web_results = []

        for link in results["organic_results"]:
            web_results.append({"link": link["link"]})

        for j in range(1, 7):
            await message.channel.send(web_results[j]["link"])
        await message.channel.send(
            "Here you go.\nHave any more questions:question:\nFeel free to ask again :smiley: !"
        )


client.run(my_secret)
