# TokyoExpress's Screenshot Scraper for Video Game Data Collection

import requests
import json
import os

ACCESS_TOKEN = "Bearer sywmvsllyn7tzyftchqn0ix6n2yqk1"
CLIENT_ID = "v2jsdlenvjxlam0frti23cgij8hoa5"

gamesfile = open("games.json", "r")
games = json.load(gamesfile)

headers = {"Authorization": ACCESS_TOKEN, "Client-ID": CLIENT_ID}

params = {"game_id": 509658, "first": "100"}
response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params)

page = 0

while page < 30:

	data = response.json()['data']
	for j, entry in enumerate(data):
		image = requests.get(entry['thumbnail_url'])

		# index = response.json()['data'][j]['thumbnail_url'].find("preview-")
		imageurl = response.json()['data'][j]['thumbnail_url'][:-20] + "480x272.jpg"

		image = requests.get(imageurl)

		filename = "presivir/Games by Gameness/Not Game/a" + str(100*page+j).zfill(4) + ".jpg"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, "wb") as file:
			file.write(image.content)
			file.close()

	if not response.json()['pagination']:
		break

	params = {"game_id": 509658, "after": response.json()['pagination']['cursor'], "first": "100"}
	response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params)
	page += 1
	print("Page " + str(page))

# Just Chatting: 509658
# Talk Shows: 417752
# index = response.json()['data'][0]['thumbnail_url'].find("preview-")
# final = response.json()['data'][0]['thumbnail_url'][:index+8] + "220x148.jpg"
# print(final)