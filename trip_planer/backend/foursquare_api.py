import requests

def fetch_places_data(destination, client_id, client_secret):
    url = 'https://api.foursquare.com/v2/venues/explore'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'v': '20210323',
        'near': destination,
        'limit': 50
    }

    response = requests.get(url, params=params)
    data = response.json()

    places_data = []
    if data['meta']['code'] == 200:
        venues = data['response']['groups'][0]['items']
        for venue in venues:
            place_info = {
                'destination': destination,
                'place': venue['venue']['name'],
                'category': venue['venue']['categories'][0]['name'],
                'cost': 0  # Cost information is not typically provided by Foursquare
            }
            places_data.append(place_info)
    return places_data
