import requests
from flask import current_app


def get_carbon_estimate(estimate_type, data):
    api_key = current_app.config['CARBON_INTERFACE_API_KEY']
    base_url = "https://www.carboninterface.com/api/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    endpoint = f"{base_url}/estimates"

    payload = {
        "type": estimate_type,
        "electricity_unit": "kwh",
        "country": data.get('country'),
        "state": data.get('state'),
        "electricity_value": data.get('electricity_usage'),
        "weight_unit": "kg",
        "weight_value": data.get('weight'),
        "distance_unit": "km",
        "distance_value": data.get('distance'),
        "transport_method": data.get('method'),
        "passengers": data.get('passengers'),
        "legs": [
            {
                "departure_airport": data.get('departure_airport'),
                "destination_airport": data.get('destination_airport')
            }
        ],
        "distance_value": data.get('distance_km'),
        "vehicle_make": data.get('vehicle_make'),
        "vehicle_model": data.get('vehicle_model'),
        "vehicle_year": data.get('vehicle_year'),
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json()