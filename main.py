import discord
import json
import os
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

PREFIX = config['bot_prefix']
TOKEN = config['bot_token']

bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    print("Main Bot is now online")


for file in os.listdir('./modules'):
    if file.endswith('.py'):
        bot.load_extension(f'modules.{file[:-3]}')
        print(f'Loaded {file}!')


bot.run(TOKEN)