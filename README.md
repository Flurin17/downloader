# Plex-Downloader

Downloads Movies (and TV-Shows) from a certain website and adds them to the Plex Media Server of a Synology NAS when a User sends a request in Discord.

## Usage:
### Movies:
- !movie [movie name]
- Select Movie by sending a number from 0 to N (Already downloaded Movies are striked through)
- If there's a Torrent available it will select the best and automatically download it
- Progress on the download is updated via the message every 10s

### TV-Shows:
- !show [tv show]
- Select TV Show by sending a number from 0 to N
- Select a season
- Select an episode (If already downloaded striked through) or a full season pack (If unavailable striked through)
- If there's a Torrent available it will select the one with the most seeders and automatically download it
- Progress on the download is updated via the message every 10s

## APIs:
- IMDB (RapidAPI)
- Discord Py
- RARBG
- Synology Download Station
- Plex

## Setup:
 - RapidAPI
 Please use the same API that we used for this project, so everything runs flawlessly.Link: https://rapidapi.com/apidojo/api/imdb8
 - Plex Tokens
 Get the Plex Tokens with the following tutorial: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
 - Downloadstation
 Setup the Downloadstation and unfortunately you must use the adminuser of the diskstation.
 - Discordbot
 Create a discord bot and server. https://discordpy.readthedocs.io/en/latest/discord.html Easiest way is to just set administrator rights, but for general safety purposes give the bot only the necessary "Text" permissions
 -Discord Channel I D
 Get the channel ID where you want your bot to work. https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord
 - Copy all the gathered data in the cred.py file
