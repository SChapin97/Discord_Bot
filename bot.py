#! /usr/bin/python3

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import datetime as dt
import asyncio
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OCTOPRINT_TOKEN = os.getenv('OCTOPRINT_TOKEN')
octoprint_url = "http://192.168.1.106"
headers  = {'Accept': 'application/json', 'x-api-key': OCTOPRINT_TOKEN}
print_is_complete = True


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

### Tests and helper functions
@bot.command(name='yeet', help='get yeeted, son')
async def yeet(ctx):
    output = "yeetus"
    await ctx.send(output)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise discord.DiscordException



### Reddit functions
@tasks.loop(hours=24)
async def send_multireddit_mail():
    message_channel = bot.get_channel(823210936311087105)
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

@tasks.loop(seconds=60)
async def send_subreddit_alert():
    message_channel = bot.get_channel(824053467182006282)
    output = os.popen('cd /home/schapin/Scripts/Reddit-Scraper/; python3 subreddit_watcher.py buildapcsales homelabsales').read()
    if output:
        for item in output.split('<end_item>\n'):
            if item.strip():
                await message_channel.send(item)


@send_multireddit_mail.before_loop
async def before_multireddit_mail():
    await bot.wait_until_ready()
    for _ in range(60*60*24):
        if dt.datetime.now().hour == 6: #Send it out at 6AM
            print('Time to send the mail out')
            return
        await asyncio.sleep(30)

@send_subreddit_alert.before_loop
async def before_subreddit_alert():
    await bot.wait_until_ready()



### Octoprint functions
@bot.command(name='print', help='Get the status of the current print job from Octoprint.')
async def print_status(ctx):
    response = requests.get(octoprint_url + "/api/job", headers=headers)

    if response.status_code == 200:
        print_name = response.json().get("job").get("file").get("name")

        if response.json().get("progress").get("printTimeLeft") == 0:
            output = f"Print {print_name} is complete."
        else:
            complete_percent = int(response.json().get("progress").get("completion"))
            time_left = format(response.json().get("progress").get("printTimeLeft") / 3600, '.2f')
            time_used = format(response.json().get("progress").get("printTime") / 3600, '.2f')
            output=(
f'''Print Name: {print_name}
{complete_percent}% Complete
Time until print is done: {time_left} hours
Print Time: {time_used} hours''')
    else:
        output = f"Connection to octoprint has failed: {response}"

    await ctx.send(output)

@tasks.loop(seconds=60)
async def alert_print_complete():
    message_channel = bot.get_channel(904148267074474024)

    response = requests.get(octoprint_url + "/api/job", headers=headers)
    state = response.json().get("state")
    print_name = response.json().get("job").get("file").get("name")

    if response.status_code == 200:
        global print_is_complete

        #Octoprint is working
        if not print_is_complete:
            if state == "Operational":
                print_is_complete = True
                await message_channel.send(f"Print {print_name} is complete.")
            else:
                pass
            #     print(f"DEBUG: print {print_name} is not complete.")
        else:
            if state == "Printing":
                print_is_complete = False
    else:
        #Wait for 30 minutes before attempting to connect to octoprint again
        asyncio.sleep(1800)

@alert_print_complete.before_loop
async def before_alert_print_complete():
    await bot.wait_until_ready()

send_multireddit_mail.start()
send_subreddit_alert.start()
alert_print_complete.start()

bot.run(TOKEN)
