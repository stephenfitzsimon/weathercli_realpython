#weather.py ap
#made following RealPython tutorial: https://realpython.com/build-a-python-weather-app-cli/#step-1-get-access-to-a-suitable-weather-api

import argparse #use to parse CLI input
import json
import sys #to use sys.exit()
from configparser import ConfigParser#used to parse the config ini file with api key
from urllib import error, parse, request #handle http errors, helps sanitize user input for use by the api, and then retrieve url info

import style

BASE_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


def read_user_cli_args():
    '''Handles user CLI input. Returns a populated namespace'''
    parser = argparse.ArgumentParser(
        description="gets weather information for a city"
    )
    #define two arguments the user can pass to the function
    parser.add_argument(
        #city argument takes one or more arguments seperated by whitespace
        #nargs='+' allows input like New York
        'city', nargs='+', type=str, help='enter a city name'
    )
    parser.add_argument(
        #optional argument to display in metric units.
        #store_true means that the default is false, but with the flag
        #will be true
        '-m',
        '--metric',
        action='store_true',
        help='display temperature in metric units'
    )
    return parser.parse_args()

def build_weather_query(city_input, metric=False):
    '''Build the url to send to the api

        Args:
            city_input (List(str)): name collected from argparse
            imperial (bool): whether (!) or not to use imperial units

        Returns:
            str: URL formatted for a call to OpenWeather API
    '''
    api_key = _get_api_key() #fetch user api
    #concatenate with a seperating whitespace, remember that
    #the city_input is a list of str
    city_name = " ".join(city_input) 
    #html encodes the city_name, and replaces whitespaces with quotes
    url_encoded_city_name = parse.quote_plus(city_name)
    units = 'metric' if metric else 'imperial'
    #build the url with str formatting
    url = (
        f'{BASE_WEATHER_API_URL}?q={url_encoded_city_name}'
        f'&units={units}&appid={api_key}'
    )
    return url

def _get_api_key():
    '''Fetch the api key from the INI config file
        Expects the file name to be secrets.ini'''
    #make a config parser object
    config = ConfigParser()
    #read the object
    config.read('secrets.ini')
    #return the key by the section number then the key value
    return config['openweather']['api_key']

def _select_weather_display_parameters(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else:
        display_params = ("🌈", style.RESET)
    return display_params


def get_weather_data(query_url):
    '''Make a url request to the API
    
        Args:
            query_url (str): url ready to pass to the open weather api
            
        Returns:
            dict: weather information for a city
    '''
    #might get a bad response if there is no city found, use a try except
    try:
        response = request.urlopen(query_url) #make an HTTP GET request
    except error.HTTPError as http_error:
        #got an error, display error type message and exit
        if http_error.code == 401: #access denied error code
            sys.exit('Access Denied. Check API key')
        elif http_error.code == 404: #404 not found
            sys.exit('Can''t find weather data for this city') 
        else:
            sys.exit(f'Something went wrong... ({http_error.code})')
    data = response.read() #extract data
    try:
        return json.loads(data) #return a python object holding JSON data
    except json.JSONDecodeError: 
        #python could not correctly read the server response
        sys.exit('Couldn''t read server response')

def display_weather_info(weather_data, metric=False):
    '''Formats weather data for display
    
        Args:
            weather_data (dict): API response containing data
            imperial (bool): whether or not to display in imperial units
            
        more info: https://openweathermap.org/current#name
    '''
    city = weather_data['name']
    weather_id = weather_data['weather'][0]['id']
    weather_desciption = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)
    weather_symbol, color = _select_weather_display_parameters(weather_id)
    style.change_color(color)
    print(f"\t{weather_symbol}", end=" ")
    print(f"{weather_desciption.capitalize():^{style.PADDING}}", end=" ")
    style.change_color(style.RESET)
    print(f"({temperature}° {'C' if metric else 'F'})")

if __name__ == '__main__':
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.metric)
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data, user_args.metric)