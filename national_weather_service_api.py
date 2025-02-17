import requests
import json

"""
This script calls the National Weather Service API and extracts the location and detailed forcast of the weather
from the returned json. The input is a set of lat/long coordinates. This can be run as a stand alone script, 
or can be used alongside the weather_app.py script.
"""

def call_api(coordinates: str) -> str:
    """
    First calls the API to get the metadata about a location using the
    x and y coordinates. Then uses the gridID of the local forcast office,
    together with the forcast office's grid points to request a weather
    forcast for the location. Then the forcast information is returned.
    """
    # Call the API to get necessary metadata needed for the forcast API call
    metadata_endpoint = 'https://api.weather.gov/points/'
    metadata_object = requests.get(metadata_endpoint + coordinates)
    metadata_text = metadata_object.text
    metadata_dict = json.loads(metadata_text)
    city = metadata_dict['properties']['relativeLocation']['properties']['city']
    state = metadata_dict['properties']['relativeLocation']['properties']['state']
    location = city +', ' + state

    # Call the API to get the weather forcast
    gridId = metadata_dict['properties']['gridId']
    gridX = str(metadata_dict['properties']['gridX'])
    gridY = str(metadata_dict['properties']['gridY'])
    base_endpoint = 'https://api.weather.gov/gridpoints/'
    full_endpoint = base_endpoint +  gridId + '/' + gridX + ',' + gridY + '/' 'forecast'
    forecast_object = requests.get(full_endpoint)
    forecast_text = forecast_object.text
    forecast_dict = json.loads(forecast_text)
    string_forcast = forecast_dict['properties']['periods'][0]['detailedForecast']
    # Make the forcast print each sentence on a new line to make it more readable
    string_forcast = string_forcast.replace('.', '.\n')
    return f'Location: \n {location}\nForcast: \n {string_forcast}'

if __name__ == '__main__':
    print('''+-----------------------------------------------------------------------------------------------------------------------------+
| This script reaches out to the National Weather Service API and returns a detailed forcast.                                 |
| It expects the Lat/Long coordinates of the location being searched.                                                         |
| Example of expected input:                                                                                                  |
|     Enter the x coordinate:   47.0357 <-- the API doesn’t support more than four decimal places of precision in coordinates |
|     Enter the y coordinate:  -122.9048                                                                                      |
+-----------------------------------------------------------------------------------------------------------------------------+\n\n''')
    while True:
        x_coordinate = input('Enter the x coordinates:\n ').strip()
        y_coordinate = input('Enter the y coordinates:\n ').strip()
        try:
            x = float(x_coordinate)
            y = float(y_coordinate)
            print('\n\n')
            pass
        except ValueError:
            print('You must enter decimal coordinates. Please try again.\n')
            del (x_coordinate, y_coordinate)
            continue

        joined_coordinates = ','.join([x_coordinate, y_coordinate])
        print(call_api(joined_coordinates))
