import requests
import streamlit as st
import pandas as pd

# Your API key
api_key = 'lSu33p5drHdIaM3j25jlOyJKp9dI4XTQ'

def get_insider_roster(symbol, api_key):
    base_url = 'https://financialmodelingprep.com/api/v4/insider-roaster'
    params = {'symbol': symbol, 'apikey': api_key}
    response = requests.get(base_url, params=params)
    print("Insider Roster Response:", response.text)  # Logging the raw response
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print(f"Error fetching insider roster for {symbol}: {response.status_code}")
        return pd.DataFrame()

def get_insider_trade_statistics(symbol, api_key):
    base_url = 'https://financialmodelingprep.com/api/v4/insider-roaster-statistic'
    params = {'symbol': symbol, 'apikey': api_key}
    response = requests.get(base_url, params=params)
    print("Insider Trade Stats Response:", response.text)  # Logging the raw response
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print(f"Error fetching trade statistics for {symbol}: {response.status_code}")
        return pd.DataFrame()

# Use the functions to get data and filter for NASDAQ exchange
symbol = 'AAPL'
insider_roster = get_insider_roster(symbol, api_key)
insider_trade_stats = get_insider_trade_statistics(symbol, api_key)

# Display the data in Streamlit
if not insider_roster.empty:
    st.write("Insider Roster for", symbol)
    st.dataframe(insider_roster)
else:
    st.error("No insider roster data available.")

if not insider_trade_stats.empty:
    st.write("Insider Trade Statistics for", symbol)
    st.dataframe(insider_trade_stats)
else:
    st.error("No insider trade statistics data available.")
