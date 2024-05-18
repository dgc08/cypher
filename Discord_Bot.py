from classes import Logger

import discord
from discord.ext import commands

import asyncio
import random
import time
import threading

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

channel_id = 1240649755143438468
bot = commands.Bot(command_prefix='!', intents=intents)
bot_status = False

with open("token.txt") as f:
    for line in f.readlines():
        if line.startswith("#") or line.strip() == "":
            pass
        else:
            token = line.strip()
            break


eventqueue = []
@bot.event
async def on_ready():
    #await bot.change_presence(status=discord.Status.invisible)
    print("Ready.")
    channel = bot.get_channel(channel_id)
    await channel.send("Cypher Security System started and ready.")
    await channel.send("https://tenor.com/view/cypher-valorant-cypher-valorant-gif-26060744")

    # Copied from another one of my projects
    global eventqueue
    global bot_status
    bot_status = True
    while True:
        while eventqueue == []:
            await asyncio.sleep(0.1)

        id = eventqueue[0][3]
        result = await eventqueue[0][0](*eventqueue[0][1], **eventqueue[0][2])
        eventqueue[0].append(result)
        try:
            while eventqueue[0][3] == id:
                await asyncio.sleep(0.1)
        except IndexError:
            pass

# Copied from another one of my projects
def run(func, *args, **kwargs):
        global eventqueue
        id = random.randint(1, 2147483647)
        eventqueue.append([func, args, kwargs, id])
        while eventqueue[0][3] != id and len(eventqueue[0]) < 5:
            time.sleep(0.1)
        while len(eventqueue[0]) == 4:
            time.sleep(0.1)
        result = eventqueue[0][4]
        eventqueue.pop(0)
        return result

class Discord_Bot(Logger):
    def log(self, event):
        # Just print log but in dc for now, will change later (TODO)
        msg = event.__str__()
        channel = bot.get_channel(channel_id)
        run(channel.send, msg)


    def __init__(self):
        def run_bot():
            bot.run(token)

        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()

        while not bot_status:
            time.sleep(0.1)


if __name__ == "__main__":
    logger = Discord_Bot()
    print()
    logger.log("\nOne of my cameras is broken!- Oh, wait, okay. It's fine.")
    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        exit()