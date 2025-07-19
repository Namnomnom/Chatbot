import requests
    
    
def get_weather_forecast(location):
    """
    Retrieves the weather forecast for a given location.

    Args:
        location (str): The location for which to retrieve the weather forecast.

    Returns:
        str: The weather forecast for the specified location.

    Raises:
        Exception: If an error occurs while retrieving the weather forecast.
    """
    
    # extract city from input string
    #format of input string: city: city_name , date:dd-mm-yyyy , location: location_name
    input_string = location
    key_value_pairs = [pair.strip() for pair in input_string.split(',')]
    extracted_values = {}
    for pair in key_value_pairs:
        if ':' in pair:
            key, value = [item.strip() for item in pair.split(':')]
            extracted_values[key] = value
        else:
            print(f"Warning: Expected a ':' in {pair}")

    city = extracted_values.get('city', '')
    
    #get the weather forecast for the city
    
    try:
        url = f"https://open-weather13.p.rapidapi.com/city/{city}"

        headers = {
            "X-RapidAPI-Key": "d9f93d0cbbmsh6495b8b1beac76ep1b16e9jsn4956b21abca2",
            "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        weather_data=response.json()
        #format the weather data to be displayed
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']
        
        #return the weather forecast in response format
        
        if response.status_code == 200:
            return f"Weather in {weather_data['name']} - Temperature: {temperature}°F, Description: {description}, Wind Speed: {wind_speed} mph, Humidity: {humidity}%"
        else:
            return f"Error: {response.status_code}"
        
    except Exception as e:
        return f"An error occurred: {str(e)}"
    