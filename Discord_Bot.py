# For the logger class you have to go a bit down

from classes import Logger

import discord
from discord.ext import commands

import asyncio
import random
import time
import threading
import uuid

from os import remove

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

channel_id = 1240649755143438468 # The text channel we want our stuff to go in
bot = commands.Bot(command_prefix='!', intents=intents)
bot_status = False

# Keep track of if laser_esp is activated or not
# If you change the status of laser_esp per hand, info_command() will produce wrong results
act_mirror = True

activate_fucntion = lambda x: None

# API token for the bot
with open("token.txt") as f:
    for line in f.readlines():
        if line.startswith("#") or line.strip() == "":
            pass
        else:
            token = line.strip()
            break

# Helper function to send an image with a text
async def send_image(filename, text, channel):
    # send image with discord.py
    await channel.send(text, file=discord.File(filename))
    # delete the file
    remove(filename)

eventqueue = []
# executed once the bot is logged in
@bot.event
async def on_ready():
    #await bot.change_presence(status=discord.Status.invisible)
    print("Ready.")
    channel = bot.get_channel(channel_id)
    await channel.send("Cypher Security System started and ready.")
    # No spam pls
    #await channel.send("https://tenor.com/view/cypher-valorant-cypher-valorant-gif-26060744")

    # Copied from another one of my projects. Look at the definition of run()
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

# Now all the text commands of the bot follow, which you execute by "!{command name}" in discord


def info(ctx):
    return f"Cypher Security System\nLaser is {act_mirror}"

@bot.command(
    name="info"
)
async def info_command(ctx):
    msg = info(ctx)
    await ctx.send(msg)

# That is only for testing. In a real system, this would be either entirely removed or not that easily executable
# I was just tired of loggin onto SSH all the time
@bot.command(
    name="poweroff"
)
async def power(ctx):
    await ctx.send(poweroff)
    import os
    os.system("poweroff")

@bot.command(
    name="deactivate"
)
async def deactivate(ctx):
    activate_function(False)
    act_mirror = False
    await ctx.send("Deactivated tripwire.")

@bot.command(
    name="activate"
)
async def activate(ctx):
    activate_function(True)
    act_mirror = True
    await ctx.send("Activated tripwire.")

# Copied from another one of my projects. You can't run async functions from within an non-async context, that's why you have this
# It queues the async function to be run in on_ready()
def run(func, *args, **kwargs):
    global eventqueue
    id = uuid.uuid4()
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
        channel = bot.get_channel(channel_id) # The text channel we want our stuff to go in
        # In case of the event just being a string instead of an event
        if type(event) == str:
            msg = event.__str__()
            run(channel.send, msg)
            return

        # If the tripwire triggers more than one time in 5 seconds, don't send it to Discord
        event.timestamp = int(event.timestamp)
        if ((time.time() - self.last_log) < 5):
            if event.monitor_origin == "cam":
                remove(event.data) # Delete file
            return
        elif event.monitor_origin == "cam":
            self.last_log = time.time()

        if (event.event_type != 1): # if Component not activated
            return

        # Ignore the laser_esp, only send the image
        if event.monitor_origin == "laser_esp":
            #run(channel.send, f"Got you! Tripwire triggered on <t:{event.timestamp}>")
            pass
        if event.monitor_origin == "cam":
            # Queue my send_image helper fucntion to be run (look at run())
            # event.data = filename of image
            run(send_image, event.data ,f"Got you! <t:{event.timestamp}>", channel)

        print ("Send something to DC")

    def __init__(self, func):
        global activate_function
        activate_function = func # Function to activate/deactivate the tripwire
        def run_bot():
            bot.run(token)

        # Start the bot
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()

        # Block thread while bot not ready
        while not bot_status:
            time.sleep(.1)

        self.last_log = -1

# To test the bot
if __name__ == "__main__":
    logger = Discord_Bot(lambda x: print("ez", x))
    logger.log("\nOne of my cameras is broken!!!- Oh, wait, okay. It's fine.")
    print()
    #logger.log()
    try:
        while 1:
            time.sleep(0.1)
    except KeyboardInterrupt:
        exit()
