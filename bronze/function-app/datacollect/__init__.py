import logging
import requests
import json
import os
import azure.functions as func  
from azure.functions import HttpRequest, HttpResponse

def get_weather(city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        #"key": os.environ.get("WEATHER_API_KEY", ""),  # clé API via env var
        "key": "4dec28902a7040929ca70430232812",
        "q": city
    }
    response = requests.get(url, params=params)
    return response.json()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function météo déclenchée')

    try:
        body = req.get_json()
        villes = body.get("villes", ["Paris", "Lille", "Amiens"])
    except:
        villes = ["Paris", "Lille", "Amiens"]

    resultats = []

    for ville in villes:
        data = get_weather(ville)
        resultats.append({"ville": ville, "data": data})

    return func.HttpResponse(json.dumps(resultats), mimetype="application/json")