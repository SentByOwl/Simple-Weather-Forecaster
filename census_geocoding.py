import requests
import json

"""
This script retrieves the lat/long coordinates of a given address using the US Census geocoding API.
It expects a full US address.
"""

def remove_excess_decimal_numbers(x_coordinate: str, y_coordinate: str) -> list:
    """
    The function take both the x and y coordinates and shortens length of the decimals to 4 decimal places.
    The 4 decimal length is a limitation of the National Weather Service API.
    """
    # This group removes the extra decimals from the x coordinate. It leaves only 4 decimal places.
    x_coordinate_separated = x_coordinate.split('.')
    x_coordinate_whole = x_coordinate_separated[0]
    x_coordinate_decimals = x_coordinate_separated[1]
    x_coordinate_decimals = list(x_coordinate_decimals)
    x_coordinate_decimals_shortened = x_coordinate_decimals[slice(0, 4)]
    x_coordinate_decimals_shortened = ''.join(x_coordinate_decimals_shortened)
    x_coordinate_fixed = x_coordinate_whole + '.' + x_coordinate_decimals_shortened

    # This group removes the extra decimals from the y coordinate. It leaves only 4 decimal places.
    y_coordinate_separated = y_coordinate.split('.')
    y_coordinate_whole = y_coordinate_separated[0]
    y_coordinate_decimals = y_coordinate_separated[1]
    y_coordinate_decimals = list(y_coordinate_decimals)
    y_coordinate_decimals_shortened = y_coordinate_decimals[slice(0, 4)]
    y_coordinate_decimals_shortened = ''.join(y_coordinate_decimals_shortened)
    y_coordinate_fixed = y_coordinate_whole + '.' + y_coordinate_decimals_shortened

    shortened_coordinates = [x_coordinate_fixed, y_coordinate_fixed]
    return shortened_coordinates

def call_api(address: str) -> list:
    """
    Calls the US Census geocoding api to get the latitude/longitude coordinates
    from a United States address.
    """
    # Format the address so that it can be accepted by the US Census geocoding API
    address_change_spaces = address.replace(' ', '+')
    address_change_commas = address_change_spaces.replace(',', '%2C')
    url = f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address_change_commas}&benchmark=4&format=json'
    geocode_object = requests.get(url)
    geocode_text = geocode_object.text
    geocode_dict = json.loads(geocode_text)
    x_coordinate = str(geocode_dict['result']['addressMatches'][0]['coordinates']['x'])
    y_coordinate = str(geocode_dict['result']['addressMatches'][0]['coordinates']['y'])

    return remove_excess_decimal_numbers(x_coordinate, y_coordinate)

if __name__ == '__main__':
    address = input('Enter address to receive lat/long coordinates: ')
    print(call_api(address))
