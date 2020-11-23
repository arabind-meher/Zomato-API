import requests
import json
import yaml

credentials = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)


class ZomatoAPI:
    def __init__(self):
        self.header = {
            "User-agent": "curl/7.43.0",
            "Accept": "application/json",
            "user_key": credentials['api']
        }

    def __repr__(self):
        pass

    def location(self, location):
        url = f'https://developers.zomato.com/api/v2.1/locations?query={location}'
        response = requests.get(url, headers=self.header)
        response_json = json.loads(response.text)

        location_dict = dict()
        location_dict['city_id'] = response_json['location_suggestions'][0]['city_id']  # City ID
        location_dict['city_name'] = response_json['location_suggestions'][0]['city_name']  # City Name
        location_dict['country_id'] = response_json['location_suggestions'][0]['country_id']  # Country ID
        location_dict['country_name'] = response_json['location_suggestions'][0]['country_name']  # Country Name
        location_dict['entity_id'] = response_json['location_suggestions'][0]['entity_id']  # Entity ID
        location_dict['entity_type'] = response_json['location_suggestions'][0]['entity_type']  # Entity Name
        location_dict['latitude'] = response_json['location_suggestions'][0]['latitude']  # Latitude
        location_dict['longitude'] = response_json['location_suggestions'][0]['longitude']  # Longitude

        return location_dict

    def location_details(self, entity_id, entity_type):
        url = f'https://developers.zomato.com/api/v2.1/location_details?entity_id={entity_id}&entity_type={entity_type}'
        response = requests.get(url, headers=self.header)
        response_json = json.loads(response.text)

        restaurants = list()
        best_rated_restaurant = response_json['best_rated_restaurant']
        for i in range(0, 10):
            res_details = list()
            if '.' not in best_rated_restaurant[i]['restaurant']['thumb']:
                continue

            # Image
            res_details.append(best_rated_restaurant[i]['restaurant']['thumb'])

            # Name
            res_details.append(best_rated_restaurant[i]['restaurant']['name'])

            # Cuisines
            res_details.append(best_rated_restaurant[i]['restaurant']['cuisines'].split(', '))

            # Establishment
            establishments = list()
            n = len(best_rated_restaurant[i]['restaurant']['establishment'])
            for j in range(n):
                establishments.append(best_rated_restaurant[i]['restaurant']['establishment'][j])
            res_details.append(establishments)

            # Highlights
            highlights = list()
            n = len(best_rated_restaurant[i]['restaurant']['highlights'])
            for j in range(n):
                highlights.append(best_rated_restaurant[i]['restaurant']['highlights'][j])
            res_details.append(highlights)

            # Rating
            rating = list()
            rating.append(best_rated_restaurant[i]['restaurant']['user_rating']['aggregate_rating'])
            rating.append(best_rated_restaurant[i]['restaurant']['user_rating']['rating_color'])
            res_details.append(rating)
            
            restaurants.append(res_details)

        return restaurants

    def restaurant(self, res_id):
        url = f'https://developers.zomato.com/api/v2.1/restaurant?res_id={res_id}'
        response = requests.get(url, headers=self.header)
        response_json = json.loads(response.text)

        return response_json
