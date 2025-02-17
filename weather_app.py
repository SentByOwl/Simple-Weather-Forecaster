import census_geocoding
import national_weather_service_api

"""
This script prints the weather forcast of a given address using the National Weather Service API.
Enter full US address.
"""

print('\n--Pull weather data from the National Weather Service API--\n')
while True:
    address = input('Enter the address that you want weather data from: \n')
    # Use the US Census geocoding API to get Lat/Long coordinates from an Address
    coordinates = census_geocoding.call_api(address)
    # The first National Weather Service API call requires the format {Lat},{Long}, which is {y},{x}. The results
    # returned by the US Census geocoding API are given in the {x},{y} format. So we need to reverse them.
    coordinates = coordinates[::-1]
    coordinates = ','.join(coordinates)
    # Finally we pass those coordinates to the National Weather Service API and return
    # a string extracted from the response that is a detailed forcast of the current weather
    print(national_weather_service_api.call_api(coordinates))
