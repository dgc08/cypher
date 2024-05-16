import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

channel = "1240649755143438468"
bot = commands.Bot(command_prefix='$', intents=intents)

class Discord_Bot(Logger):
    pass
