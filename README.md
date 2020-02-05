# Plex-Downloader

Downloads Movies (and TV-Shows) from a certain website and adds them to the Plex Media Server of a Synology NAS when a User sends a request in Discord.

## Usage:
- !movie [movie name]
- Select Movie by sending a number from 0 to N (Already downloaded Movies are striked through)
- If theres a Torrent available it will select the best and automatically download it
- Progress on the download is updated via the message every 10s

- !show [tv show]
- Select TV Show by sending a number from 0 to N
- Select a season
- Select an episode (If already downloaded striked through) or a full season pack (If unavailable striked through)
- If theres a Torrent available it will select the one with the most seeders and automatically download it
- Progress on the download is updated via the message every 10s

## APIs:
- IMDB (RapidAPI)
- Discord Py
- RARBG
- Synology Download Station
- Plex
