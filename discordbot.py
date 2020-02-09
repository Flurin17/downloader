import discord
from discord.ext import commands
from plexdownloader.cred import *
from plexdownloader.downloadermain import *

bot = commands.Bot(command_prefix='!')

bot.load_extension('plexdownloader.downloadermain')

bot.run(discordBotToken)