#! /usr/bin/python3

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import datetime as dt
import asyncio
import requests
import subprocess

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#OCTOPRINT_TOKEN = os.getenv('OCTOPRINT_TOKEN')
#OCTOPRINT_URL = os.getenv('OCTOPRINT_URL')
#PRINT_CHANNEL = os.getenv('PRINT_CHANNEL')
#HOME_COMMAND = os.getenv('HOME_COMMAND')
#HOME_CHANNEL = os.getenv('HOME_CHANNEL')
ALAMO_COMMAND = os.getenv('ALAMO_COMMAND')
ALAMO_CHANNEL = os.getenv('ALAMO_CHANNEL')
NOTIFY_FILE = os.getenv('NOTIFY_FILE')
NOTIFY_CHANNEL = os.getenv('NOTIFY_CHANNEL')
SUBREDDIT_COMMAND = os.getenv('SUBREDDIT_COMMAND')
SUBREDDIT_CHANNEL = os.getenv('SUBREDDIT_CHANNEL')
#MULTIREDDIT_COMMAND = os.getenv('MULTIREDDIT_COMMAND')
#MULTIREDDIT_CHANNEL = os.getenv('MULTIREDDIT_CHANNEL')

headers  = {'Accept': 'application/json', 'x-api-key': OCTOPRINT_TOKEN}
print_is_complete = True

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

###################################
#### Bot boilerplate functions ####
###################################

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(f'{bot.user} is connected to guild: '
    f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    send_subreddit_alert.start()
#    alert_print_complete.start()
    read_notification_messages.start()
    alamo_drafthouse_notifications.start()

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise discord.DiscordException


###########################
#### Command functions ####
###########################

### More or less a check to see if the bot is online
@bot.command(name='yeet', help='get yeeted, son')
async def yeet(ctx):
    output = "yeetus"
    await ctx.send(output)


### On demand see who is on the home wifi
@bot.command(name='home', help='Tells you who is connected to the home wifi')
async def who_is_home(ctx):
    message_channel = bot.get_channel(int(HOME_CHANNEL))
    output = subprocess.check_output(HOME_COMMAND, shell=True, text=True)
    if output:
        await message_channel.send(output)
    else:
        await message_channel.send("No one is home.")

### Octoprint (3D printing software) status
@bot.command(name='print', help='Get the status of the current print job from Octoprint.')
async def print_status(ctx):
    response = requests.get(OCTOPRINT_URL + "/api/job", headers=headers)

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


#####################################
#### Looped, automated functions ####
#####################################

### Look for new alamo drafthouse movies

@tasks.loop(hours=12)
async def alamo_drafthouse_notifications():
    message_channel = bot.get_channel(int(ALAMO_CHANNEL))
    output = subprocess.check_output(ALAMO_COMMAND, shell=True, text=True)
    if output:
        await message_channel.send(output)

@alamo_drafthouse_notifications.before_loop
async def before_alamo_drafthouse_notifications():
    await bot.wait_until_ready()


### Read notification messages
@tasks.loop(seconds=15)
async def read_notification_messages():
    message_channel = bot.get_channel(int(NOTIFY_CHANNEL))

    with open(NOTIFY_FILE, 'r+') as file:
        output = file.read()
        if output:
            await message_channel.send(output)
            file.truncate(0)

@read_notification_messages.before_loop
async def before_read_notification_messages():
    #Create messages file if it does not exist
    if not os.path.exists(NOTIFY_FILE):
        f = open(NOTIFY_FILE, "w")
        f.close()

    await bot.wait_until_ready()


@tasks.loop(seconds=60)
async def send_subreddit_alert():
    message_channel = bot.get_channel(int(SUBREDDIT_CHANNEL))
    output = os.popen(SUBREDDIT_COMMAND).read()
    if output:
        for item in output.split('<end_item>\n'):
            if item.strip():
                await message_channel.send(item)

@send_subreddit_alert.before_loop
async def before_subreddit_alert():
    await bot.wait_until_ready()


@tasks.loop(seconds=60)
async def alert_print_complete():
    message_channel = bot.get_channel(int(PRINT_CHANNEL))

    response = requests.get(OCTOPRINT_URL + "/api/job", headers=headers)
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


#@tasks.loop(hours=24)
#async def send_multireddit_mail():
#    message_channel = bot.get_channel(int(MULTIREDDIT_CHANNEL))
#    os.system(MULTIREDDIT_COMMAND)
#    #The files will appear in <...>/Reddit-Scraper/.output/ which is symlinked in the website directory for easy access.
#    output = \"\"\"Reddit Newsfeed is now available at the following links:"\"\"
#    await message_channel.send(output)

#@send_multireddit_mail.before_loop
#async def before_multireddit_mail():
#    await bot.wait_until_ready()
#    for _ in range(60*60*24):
#        if dt.datetime.now().hour == 6: #Send it out at 6AM
#            print('Time to send the mail out')
#            return
#        await asyncio.sleep(30)



bot.run(TOKEN)
