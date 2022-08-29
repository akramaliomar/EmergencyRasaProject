import requests


def fetch_vital_signs():
    url = 'https://aceiot-project.uc.r.appspot.com/fetch_vs'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data


def fetch_aggr_signs():
    url = 'https://aceiot-project.uc.r.appspot.com/fetch_aggr_vs'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data

def fetch_heath_status():
    url = 'https://aceiot-project.uc.r.appspot.com/prediction'
    json_data = requests.get(url).json()
    # format_add = json_data['main']
    # print(format_add)
    return json_data