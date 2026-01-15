# Is my favorite Twitch streamer live?
This is a simple Python script that checks if a specified Twitch streamer is currently live. It uses the Twitch API to fetch the stream status and check whether the streamer is live or offline.

## Features
- Checks if a Twitch streamer is currently live. The user name is provided via the text file `streamer.txt`
- Opens the streamer's Twitch page in the default browser if they are live
- Check multiple streamers at once and open only the first stream that is live

## TODO
- Add error handling for network issues and invalid streamer names
- Refactor code and split into multiple files for better organization