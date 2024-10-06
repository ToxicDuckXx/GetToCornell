

import csv
import requests
import json
import math
from datetime import datetime

ROUTES_API_KEY = "AIzaSyBpihTHfvYy26ThvIvakeNrsPI6dmcL-dM"
FLIGHTS_API_KEY = "a02425033bmsheb3a4cb3ac254f0p16351fjsnc919150b9517"

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance in miles between two points 
    on the earth (specified in decimal degrees) using the Haversine formula."""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 3956  # Radius of earth in miles
    return c * r

def find_nearby_airports(lat, lon, csv_file):
    nearby_airports = []
    max_distance = 100  # Maximum distance in miles

    # Read the CSV file
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            airport_code = row[0]  # Assuming airport code is in the first column
            airport_lat = row[2]  # Latitude is in the 10th column
            airport_lon = row[3]  # Longitude is in the 12th column
            if airport_lon == "" or airport_lat == "":
                continue
            # Calculate the distance
            distance = haversine(lat, lon, float(airport_lat), float(airport_lon))
            
            # Check if the distance is within the limit
            if distance <= max_distance:
                nearby_airports.append(airport_code)
    
    return nearby_airports

# Example usage
# airport_codes = find_nearby_airports(22.37583333, 31, 'path/to/your/file.csv')
# print(airport_codes)


# Example usage
# airport_codes = find_nearby_airports(22.37583333, 31, 'path/to/your/file.csv')
# print(airport_codes)

def get_nearby_airports(lat, lng):

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getNearByAirports"

    querystring = {"lat":lat,"lng":lng,"locale":"en-US"}

    headers = {
        "x-rapidapi-key": "a02425033bmsheb3a4cb3ac254f0p16351fjsnc919150b9517",
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    skyID = response.json()["data"]["current"]["skyId"]
    entityID = response.json()["data"]["current"]["entityId"]
    return (skyID, entityID)

def get_flights(start_skyID, startId, dest_skyID, destId, date, amount):
    
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlights"

    querystring = {"originSkyId":start_skyID,"destinationSkyId":dest_skyID,"originEntityId":startId,"destinationEntityId":destId,"cabinClass":"economy","adults":"1","sortBy":"best","currency":"USD","market":"en-US","countryCode":"US","date":date,"limit":amount}

    headers = {
        "x-rapidapi-key": "a02425033bmsheb3a4cb3ac254f0p16351fjsnc919150b9517",
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    #flightsList = response.json()['data']['context']['legs']
    return response.json()

def parse_flight_data(data, data2, dir):

    json_data = data['data']['itineraries']
    json_data2 = data2['data']['itineraries']
    result = {"flights":[]}
    for route in json_data:
        if len(route["legs"]) == 1:
            dt = datetime.strptime(route["legs"][0]["departure"], "%Y-%m-%dT%H:%M:%S")
            formatted_time = dt.strftime("%I:%M %p")
            if dir == "to":
                airport = route["legs"][0]["destination"]["displayCode"]
                maps_bus_embed = f"https://www.google.com/maps/dir/?api=1&origin={airport}&destination=Cornell+University&travelmode=transit"
            else:
                airport = route["legs"][0]["origin"]["displayCode"]
                maps_bus_embed = f"https://www.google.com/maps/dir/?api=1&origin=Cornell+University&destination={airport}&travelmode=transit"
            result["flights"].append({"duration":route["legs"][0]["durationInMinutes"], "departure":formatted_time, "price":route["price"]["formatted"], "flt":route["legs"][0]["segments"][0]["flightNumber"], "airline":route["legs"][0]["carriers"]["marketing"][0]["name"], "logo":route["legs"][0]["carriers"]["marketing"][0]["logoUrl"], "origin":route["legs"][0]["origin"]["displayCode"], "dest":route["legs"][0]["destination"]["displayCode"], "embed":maps_bus_embed})
    
    for route in json_data2:
        if len(route["legs"]) == 1:
            dt = datetime.strptime(route["legs"][0]["departure"], "%Y-%m-%dT%H:%M:%S")
            formatted_time = dt.strftime("%I:%M %p")
            if dir == "to":
                airport = route["legs"][0]["destination"]["displayCode"]  
            else:
                airport = route["legs"][0]["origin"]["displayCode"]  
            maps_bus_embed = f"https://www.google.com/maps/embed/v1/directions?origin=place_id:ChIJndqRYRqC0IkR9J8bgk3mDvU-w&destination={airport}&key=AIzaSyDRPlQT-oqfn2Vkr6OBsQSfmc7q0axo8a8&mode=transit"

            result["flights"].append({"duration":route["legs"][0]["durationInMinutes"], "departure":formatted_time, "price":route["price"]["formatted"], "flt":route["legs"][0]["segments"][0]["flightNumber"], "airline":route["legs"][0]["carriers"]["marketing"][0]["name"], "logo":route["legs"][0]["carriers"]["marketing"][0]["logoUrl"], "origin":route["legs"][0]["origin"]["displayCode"], "dest":route["legs"][0]["destination"]["displayCode"], "embed":maps_bus_embed})

    return result


def dis_between_cords(lat1, lng1, lat2, lng2):

    pass

def distance(lat1, lon1, lat2, lon2):
    # Distance formula to calculate the distance between two points
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) * 69

def googleMapsBuses(airpot_code):

    airpot_data = {"JFK":("40.641766", "-73.780968"), "LGA":("40.7766", "-73.874069"), "EWR":("40.689491", "-74.174538")}

    cords = airpot_data.get(airpot_code)

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin=42.4534,-76.475266&destination={cords[0]},{cords[1]}&mode=transit&key={ROUTES_API_KEY}"
    content = requests.get(url).content
    with open("data.json", "wb") as file:
        file.write(content)
        file.close()
    json_content = json.loads(content)
    legs = json_content["routes"][0]["legs"]


print(googleMapsBuses("JFK"))

def get_flight_api(origin_city):

    url = "https://compare-flight-prices.p.rapidapi.com/GetPricesAPI/StartFlightSearch.aspx"

    querystring = {"lapinfant":"0","child":"0","city2":"NYC","date1":"2021-01-01","youth":"0","flightType":"1","adults":"1","cabin":"1","infant":"0","city1":"LAX","seniors":"0","date2":"2021-01-02","islive":"false"}

    headers = {
        "x-rapidapi-key": "a02425033bmsheb3a4cb3ac254f0p16351fjsnc919150b9517",
        "x-rapidapi-host": "compare-flight-prices.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())


def load_cities_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def distance(lat1, lon1, lat2, lon2):
    # Distance formula to calculate the distance between two points
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

def get_closest_city_codes(latitude, longitude, cities, num_results=3, max_distance=200):
    distances = []
    
    for city in cities:
        dist = distance(latitude, longitude, city['latitude'], city['longitude'])
        if dist < max_distance:
            distances.append((city['iata_code'], dist))
    
    # Sort the list by distance
    distances.sort(key=lambda x: x[1])
    
    # Get the closest num_results city codes
    closest_city_codes = [city[0] for city in distances[:num_results]]
    
    return closest_city_codes


def get_iata_code_from_address(address, date, direction):

    google_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={ROUTES_API_KEY}"

    json_content = json.loads(requests.get(google_url).content)
    lat = json_content["results"][0]["geometry"]["location"]["lat"]
    lng = json_content["results"][0]["geometry"]["location"]["lng"]
    print(f"{lat},{lng}")
   # cities = load_cities_from_file('cities2.json')
    skyId, entityId = get_nearby_airports(lat, lng)
    print(f"{skyId}, {entityId}")
    if direction == "to":
        data = get_flights(skyId, entityId, "NYCA", '27537542', date)
        data2 = get_flights(skyId, entityId, "SYR", '95674004', date, "3")
    else:
        data = get_flights("NYCA", '27537542', skyId, entityId, date)
        data2 = get_flights("SYR", '95674004', skyId, entityId, date, "3")
    return parse_flight_data(data, data2, direction)



#get_iata_code_from_address("14894 S Leland Rd, Beavercreek, OR 97004")
