import requests
import streamlit as st
import pandas as pd

# Base URL for the API request
base_url = 'https://financialmodelingprep.com/api/v3/search'

# Your API key
api_key = 'lSu33p5drHdIaM3j25jlOyJKp9dI4XTQ'
query = 'AAPL'  # Search query

# Function to get data and display in Streamlit
def get_data(query, exchange):
    params = {
        'query': query,
        'apikey': api_key
        # 'exchangeShortName': exchange  # Uncomment or modify if the API supports filtering by exchange
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        if json_data:
            # Display the raw JSON data in Streamlit
            st.json(json_data)
            
            # If you want to display it as a table and the JSON is a list of dictionaries
            df = pd.DataFrame(json_data)
            st.dataframe(df)
            return json_data
        else:
            st.write("No data found for the specified query.")
            return None
    else:
        error_message = f"An error occurred: {response.status_code} - {response.text}"
        st.error(error_message)
        return None

# Fetch and display data for NASDAQ exchange
get_data(query, 'NASDAQ')
