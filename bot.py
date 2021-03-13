#! /usr/bin/python3

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import datetime as dt
import asyncio

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

@tasks.loop(hours=24)
#@bot.command(name='mail', help='Sends mail from multireddits')
async def send_multireddit_mail():
    message_channel = bot.get_channel(812710676299644940)
    os.system('cd /home/schapin/Scripts/Reddit-Scraper/; bash mail_newsfeed_posts.sh')
    #The files will appear in <...>/Reddit-Scraper/.output/ which is symlinked in the website directory for easy access.
    output = """Reddit Newsfeed is now available at the following links:
        https://www.samuelchapin.com/reddit/dev.html
        https://www.samuelchapin.com/reddit/3DPrinting.html
        https://www.samuelchapin.com/reddit/deals.html
        https://www.samuelchapin.com/reddit/memes.html
        https://www.samuelchapin.com/reddit/mindless.html
        https://www.samuelchapin.com/reddit/misc.html
        https://www.samuelchapin.com/reddit/news.html
        https://www.samuelchapin.com/reddit/pictures.html"""
    await message_channel.send(output)



@send_multireddit_mail.before_loop
async def before_multireddit_mail():
    await bot.wait_until_ready()
    for _ in range(60*60*24):
        if dt.datetime.now().hour == 6: #Send it out at 6AM
            print('Time to send the mail out')
            return
        await asyncio.sleep(1)

send_multireddit_mail.start()

bot.run(TOKEN)
