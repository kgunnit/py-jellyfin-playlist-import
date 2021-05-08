import requests
import argparse
import os
import json
import sys

# fixme detect http / https in host
# fixme requests timeout + error log

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="m3u8 playlist input file")
parser.add_argument("playlist_name", help="playlist name to create in jellyfin")
parser.add_argument("--host", help="host ip or domain name")
parser.add_argument("--userid", help="userid hash")
parser.add_argument("--apikey", help="api key hash")
args = parser.parse_args()

host = args.host
userid = args.userid
apikey = args.apikey

track_query_url = "http://" + host + "/Items?UserId="+userid+"&format=json&api_key="+apikey+"&Recursive=true&IncludeItemTypes=Audio+MusicAlbum+MusicArtist&fields=Path&SearchTerm="
add_playlist_url = "http://" + host + "/Playlists"

input_file = args.input_file

def logmsg(status,msg):
    if (status == "info"):
        print("[*] "+msg)
    elif (status == "error" or status == "fail"):
        print(bcolors.FAIL + "[!] "+msg + bcolors.ENDC)
    elif (status == "success"):
        print(bcolors.OKGREEN + "[+] "+msg + bcolors.ENDC)

playlist_name = args.playlist_name
logmsg("info","Creating playlist: "+playlist_name)
headers = {"Content-Type": "application/json", "X-Emby-Token": apikey}
media_text = ""
media_title = ""

list_items = []
with open(input_file, "r") as input_file:
    for media_file in input_file:
        media_file = media_file.rstrip()
        if (media_file[0:7] == "#EXTINF"):
            media_text = media_file.split(",")[1]
            media_title = media_text.split(" -")[0]
            media_file = media_file.rstrip()
        if (media_file[0] != "#"):
            media_file_fullpath = media_file
            media_file = os.path.basename(media_file)
            media_file_name = os.path.splitext(media_file)[0]
            query_url = track_query_url + media_file_name
            logmsg("info","Querying track (file name): "+media_file_name)

            response = requests.get(query_url)
            response_json = json.loads(response.text)
            #logmsg("info", "Items found: "+str(len(response_json["Items"])))
            if (len(response_json["Items"]) == 0):
                query_url = track_query_url + media_title
                logmsg("fail", "Track not found, trying title")
                logmsg("info","Querying track (title): "+media_title)
                response = requests.get(query_url)
                response_json = json.loads(response.text)
                #logmsg("info", "Items found: "+str(len(response_json["Items"])))
                media_text = ""
                media_title = ""
            if (len(response_json["Items"]) > 0):
                for response_item in response_json["Items"]:
                    response_path = None
                    try:
                        response_path = response_item["Path"]
                    except:
                        logmsg("fail", "Unable to load media path")
                        print(response_item)
                    if (response_path == media_file_fullpath):
                        response_id = response_item["Id"]
                        logmsg("success","  Found match with track ID: "+response_id)
                        list_items.append(response_id)
            else:
                logmsg("fail","  Unable to find track")


logmsg("info", "Creating Playlist...")
data = {"ids": list_items, "userId": userid, "Name": playlist_name}
playlist_add_response = requests.post(url=add_playlist_url, headers=headers, data=json.dumps(data))
if (playlist_add_response.status_code == 200):
    logmsg("success","  Playlist successfully created: "+playlist_add_response.text)
else:
    logmsg("fail", "  Unable to add track")
    print(playlist_add_response.text)
