#! /usr/bin/python3

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(f'{bot.user} is connected to guild: '
    f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='yeet', help='get yeeted, son')
async def yeet(ctx):
    output = "yeetus"
    await ctx.send(output)

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#             if event == 'on_message':
#                 f.write(f'Unhanelded message: {args[0]}\n')
#             else:
#                 raise discord.DiscordException




bot.run(TOKEN)
