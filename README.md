# Discord_Bot

## Purpose
- This is a discord (social media messaging service) bot that I use to improve my digitial life via automation.
- This runs on a local server in my home where I can do things like view local network traffic and send/receive information from the wider internet.

## Functions
- The main functions of this bot is as follows:
1. Oversee 3D Printing status via Octoprint
   - This is a useful service as I can wait to get a notification from discord as to when a 3D print I started is complete, or get updates on the status of a currently running print/how long it will take to complete.
2. Alamo Drafthouse New Movies
   - This runs [another script on my github profile](https://github.com/SChapin97/alamo_drafthouse_new_movies).
   - Every 12 hours it will check for a new movie from the Woodbury, MN Alamo Drafthouse location and let me know if there are any new movies posted.
3. Read notification messages
   - This is a pretty simple script that makes server automation a whole lot easier.
   - Every 15 seconds, this will check a certain file on my server to see if it has any text content, and send it to a notification channel if it does.
   - This can be used in conjunction with other tasks, like alerting me of any S.M.A.R.T. hard drive failures or when long running tasks (like file RSYNC backups) are complete.
4. Send subreddit alerts
   - This will search for any posts on a given subreddit (or lists of subreddit) and will try to find any plaintext terms.
   - This also uses [another script I have on my github profile](https://github.com/SChapin97/Reddit-Scraper/blob/master/subreddit_watcher.py).
   - For example, I use this to search for any server deals on /r/homelabsales that are in Minnesota and /r/3dprintingdeal for any cheap 3D printing filament.
5. Send multireddit mail
   - Although I don't get much use out of this, it is used to get a full day's worth of top posts from a user's multireddit feed and host them on a website for easy viewing.
   - I used this a while ago when I was trying to wean off of social media, however I didn't find much use for it after a few weeks.
   - This also uses [another script I have in my github profile](https://github.com/SChapin97/Reddit-Scraper/blob/master/multireddit_newsfeed.py).
