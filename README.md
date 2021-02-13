# py-jellyfin-playlist-import

Original project: https://blog.project-insanity.org/2019/03/06/importing-playlists-to-jellyfin-media-server/

Repo: https://git.project-insanity.org/onny/py-jellyfin-playlist-import

## Usage

The script requires an api key which has to be created in Jellyfin and further you’ll need the user id which will then own the imported playlist.

Creating API key:
 - Go to server settings (icon upper right corner)
 - Navigate to: Expert → Advanced (left menu)
 - Navigate to: Security (menu upper middle part)
 - Beside title “api keys”, click on the plus symbol
 - App name: playlist importer
 - Copy/write down api key hash, something like a5dc4ea2f58d490db39c9e0ad204aa83

Get userid hash:
 - Click on the profile icon, upper right corner
 - Click on profile
 - Copy/write down userid hash from the url which looks like: myserver.com/web/index.html#!/myprofile.html?userId=eb8c2ec5352843d3a16ca11c26d3551c

```
git clone https://git.project-insanity.org/onny/py-jellyfin-playlist-import.git
cd py-jellyfin-playlist-import
python main.py --host "example.com" --userid "eb8c2ec5352843d3a16ca11c26d3551c" --apikey "a5dc4ea2f58d490db39c9e0ad204aa83" /tmp/rock.m3u8 rock
```
