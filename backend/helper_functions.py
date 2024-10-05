import csv
import requests
import json

ROUTES_API_KEY = "AIzaSyBpihTHfvYy26ThvIvakeNrsPI6dmcL-dM"

def googleMapsBuses(startCords, endCords):

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={startCords[0]},{startCords[1]}&destination={endCords[0]},{endCords[1]}&mode=transit&key={ROUTES_API_KEY}"
    content = requests.get(url).content
    with open("data.json", "wb") as file:
        file.write(content)
        file.close()
    json_content = json.loads(content)
    return json_content
