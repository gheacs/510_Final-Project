import requests
import streamlit as st

# Base URL for the API request
base_url = 'https://financialmodelingprep.com/api/v3/search'

# Your API key
api_key = 'lSu33p5drHdIaM3j25jlOyJKp9dI4XTQ'
query = 'AAPL'  # Search query

# Function to get data and filter for NASDAQ
def get_data(query, exchange='NASDAQ'):
    params = {
        'query': query,
        'apikey': api_key
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Manually filter results to only include those from the NASDAQ exchange
            filtered_data = [item for item in data if item['exchangeShortName'] == exchange]
            st.write(filtered_data)  # Display the filtered data in Streamlit
            return filtered_data
        else:
            st.write("No data found for the specified query.")
            return None
    else:
        error_message = f"An error occurred: {response.status_code} - {response.text}"
        print(error_message)
        st.write(error_message)
        return None

# Get data and filter for NASDAQ exchange
NASDAQ_data = get_data(query)
