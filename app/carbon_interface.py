"""
Module for interacting with the Carbon Interface API.
- Fetches the ID of a vehicle model based on make and year from the Carbon Interface API
- Sends a request to the Carbon Interface API to calculate a carbon estimate based on type and data
"""
import requests
from flask import current_app


def get_vehicle_model_id(api_key, make, model, year):
    """
    Fetches the ID of a vehicle model based on make and year from the Carbon Interface API.

    Parameters:
    api_key (str): Carbon Interface API key.
    make (str): Vehicle make.
    model (str): Vehicle model.
    year (int): Vehicle year.

    Returns:
    int: Vehicle model ID. Raises ValueError if not found.

    Raises:
    ValueError: If the vehicle make/model is not found.
    requests.exceptions.HTTPError: For HTTP request errors.
    """
    base_url = "https://www.carboninterface.com/api/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Get vehicle makes
    makes_response = requests.get(f"{base_url}/vehicle_makes", headers=headers)
    makes_response.raise_for_status()
    makes = makes_response.json()

    # Find the make ID
    make_id = next((item['data']['id'] for item in makes if item['data']['attributes']['name'].lower() == make.lower()),
                   None)

    if not make_id:
        raise ValueError(f"Vehicle make '{make}' not found")

    # Get vehicle models for the specific make
    models_response = requests.get(f"{base_url}/vehicle_makes/{make_id}/vehicle_models", headers=headers)
    models_response.raise_for_status()
    models = models_response.json()

    # Find the model ID
    model_id = next((item['data']['id'] for item in models
                     if item['data']['attributes']['name'].lower() == model.lower()
                     and item['data']['attributes']['year'] == int(year)), None)

    if not model_id:
        raise ValueError(f"Vehicle model '{model}' ({year}) not found for make '{make}'")

    return model_id


def get_carbon_estimate(estimate_type, data):
    """
    Sends a request to the Carbon Interface API to calculate a carbon estimate based on type and data.

    Parameters:
    estimate_type (str): Type of estimate ('electricity', 'flight', 'shipping', 'vehicle').
    data (dict): Data required for the estimate type:
        - 'electricity': 'electricity_unit', 'electricity_value', 'country', 'state'
        - 'flight': 'passengers', 'departure_airport', 'destination_airport', 'return_flight' (optional)
        - 'shipping': 'weight_value', 'weight_unit', 'distance_value', 'distance_unit', 'transport_method'
        - 'vehicle': 'vehicle_make', 'vehicle_model', 'vehicle_year', 'distance_value'

    Returns:
    dict: Carbon estimate from the API.

    Raises:
    requests.exceptions.HTTPError: On API request failure.
    """
    api_key = current_app.config['CARBON_INTERFACE_API_KEY']
    base_url = "https://www.carboninterface.com/api/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    endpoint = f"{base_url}/estimates"

    payload = {
        "type": estimate_type,
    }

    if estimate_type == 'electricity':
        payload.update({
            "electricity_unit": data.get('electricity_unit', 'mwh'),
            "electricity_value": data.get('electricity_value'),
            "country": data.get('country'),
            "state": data.get('state')
        })
    elif estimate_type == 'flight':
        payload.update({
            "passengers": int(data.get('passengers', 1)),
            "legs": [
                {
                    "departure_airport": data.get('departure_airport'),
                    "destination_airport": data.get('destination_airport')
                }
            ]
        })
        # Add the return flight if provided from the form.
        if data.get('return_flight'):
            payload["legs"].append({
                "departure_airport": data.get('destination_airport'),
                "destination_airport": data.get('departure_airport')
            })
    elif estimate_type == 'shipping':
        payload.update({
            "weight_value": data.get('weight_value'),
            "weight_unit": data.get('weight_unit', 'g'),
            "distance_value": data.get('distance_value'),
            "distance_unit": data.get('distance_unit', 'km'),
            "transport_method": data.get('transport_method')
        })
    elif estimate_type == 'vehicle':
        vehicle_model_id = get_vehicle_model_id(api_key, data.get('vehicle_make'), data.get('vehicle_model'),
                                                data.get('vehicle_year'))
        payload.update({
            "distance_value": data.get('distance_value'),
            "vehicle_model_id": vehicle_model_id,
            "distance_unit": data.get('distance_unit', 'mi')
        })
    elif estimate_type == 'fuel_combustion':
        payload.update({
            "fuel_source_type": data.get('fuel_source_type'),
            "fuel_source_unit": data.get('fuel_source_unit'),
            "fuel_source_value": float(data.get('fuel_source_value'))
        })

    response = requests.post(endpoint, json=payload, headers=headers)

    # Raise an exception for HTTP errors
    response.raise_for_status()
    return response.json()
