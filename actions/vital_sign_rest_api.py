import requests


def fetch_vital_signs():
    url = 'http://172.20.0.4:5000/fetch'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data

#print(weather("Delhi")[0][0])

def weather_things_speak():
    api_address = 'https://api.thingspeak.com/channels/1681090/feeds.json?api_key=JIW9H2NBKHBENWP8&results=2'

    # url = api_address + city
    json_data = requests.get(api_address).json()
    format_add = json_data['feeds']
    # print(format_add)
    return format_add[0]


# print(weather_things_speak())