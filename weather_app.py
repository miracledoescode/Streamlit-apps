import streamlit as st
import requests

def get_weather(city):
    api_key = "ab71c4062929c438b5e330984b39c620"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data["cod"] == 200:
            return data, None
        
    except requests.exceptions.HTTPError:
        error_messages = {
            400: "Bad request - Please check your input",
            401: "Unauthorized - Please check your API key",
            403: "Forbidden - Access is denied",
            404: "City not found",
            500: "Internal Server Error - Please try again",
            502: "Bad Gateway - Invalid response from server",
            503: "Service Unavailable - Server is down",
            504: "Gateway Timeout - No response from server"
        }
        return None, error_messages.get(response.status_code, f"HTTP error occurred: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        return None, "Connection Error: Check your internet connection"
    except requests.exceptions.Timeout:
        return None, "Timeout Error: The request timed out"
    except requests.exceptions.TooManyRedirects:
        return None, "Too many Redirects: Check the URL"
    except requests.exceptions.RequestException as req_error:
        return None, f"Request Error: {req_error}"

def display_weather(data):
    # Extract weather data
    temp_kelvin = data['main']['temp']
    temp_celsius = temp_kelvin - 273.15
    weather_desc = data['weather'][0]['description'].title()
    condition = data['weather'][0]['main'].lower()
    
    # Set emoji based on weather condition
    emojis = {
        'clear': '☀️',
        'clouds': '☁️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'drizzle': '🌦️'
    }
    emoji = emojis.get(condition, '🌈')
    
    return temp_celsius, weather_desc, emoji

# Streamlit UI
st.set_page_config(page_title="Weather App", page_icon="🌤️")

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .emoji-font {
        font-size:80px !important;
        text-align: center;
    }
    .desc-font {
        font-size:24px !important;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Weather App ⛅")

# Input
city = st.text_input("Enter city name:", placeholder="Type a city name...", key="city_input")

if city:
    data, error = get_weather(city)
    
    if error:
        st.error(error)
    else:
        temp_celsius, weather_desc, emoji = display_weather(data)
        
        # Display weather information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<p class="big-font">{temp_celsius:.1f}°C</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<p class="emoji-font">{emoji}</p>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<p class="desc-font">{weather_desc}</p>', unsafe_allow_html=True)
