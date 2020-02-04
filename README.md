# Plex-Downloader

Downloads Movies (and TV-Shows) from a certain website and adds them to Plex of a Synology NAS when a User sends a request in Discord.

Usage:
- !dwn [movie name]
- Select Movie by sending a number from 0 to n (Already downloaded Movies are striked through)
- If theres a T*rrent available it will select the best and automatically download it
- Progress on the download is updated via the message every 10s

APIs:
- IMDB (RapidAPI)
- Discord Py
- R*rBg
- Synology Download Station
- Plex
