# TokyoExpress's Screenshot Scraper for Video Game Data Collection

import requests
import json
import os

ACCESS_TOKEN = "Bearer sywmvsllyn7tzyftchqn0ix6n2yqk1"
CLIENT_ID = "v2jsdlenvjxlam0frti23cgij8hoa5"

gamesfile = open("games.json", "r")
games = json.load(gamesfile)

headers = {"Authorization": ACCESS_TOKEN, "Client-ID": CLIENT_ID}

for i in range(200):

	page = 0

	game = games[i]['id']
	gamename = games[i]['name']
	params = {"game_id": game, "first": "50"}
	response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params)

	while page < 1:

		data = response.json()['data']
		for j, entry in enumerate(data):
			imageurl = response.json()['data'][j]['thumbnail_url'][:-20] + "480x272.jpg"
			image = requests.get(imageurl)
			filename = "presivir/test/" + gamename.replace(":", "") + "/" + str(100*page+j).zfill(4) + ".jpg"
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			with open(filename, "wb") as file:
				file.write(image.content)
				file.close()

		if not response.json()['pagination']:
			break

		params = {"game_id": game, "after": response.json()['pagination']['cursor'], "first": "50"}
		response = requests.get("https://api.twitch.tv/helix/clips", headers=headers, params=params)
		page += 1
		print("Page " + str(page) + " of " + gamename)

# index = response.json()['data'][0]['thumbnail_url'].find("preview-")
# final = response.json()['data'][0]['thumbnail_url'][:index+8] + "220x148.jpg"
# print(final)