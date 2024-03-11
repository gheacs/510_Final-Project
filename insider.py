import finnhub
import streamlit as st
import pandas as pd

# Initialize Finnhub client with your API key
api_key = 'cnn42hhr01qq36n5lak0cnn42hhr01qq36n5lakg'  # Ensure this is your valid API key
finnhub_client = finnhub.Client(api_key=api_key)

# Function to get insider transactions
def get_insider_transactions(symbol, from_date, to_date):
    if not symbol:
        return pd.DataFrame()
    try:
        transactions = finnhub_client.stock_insider_transactions(symbol, from_date, to_date)
        if transactions and 'data' in transactions:
            df = pd.DataFrame(transactions['data'])
            st.write("Insider Transactions:", df)
            return df
        else:
            st.error(f'No insider transactions data found for{symbol}.')
            return pd.DataFrame()
    except Exception as e:
        st.error(f'An error occurred fetching insider transactions for {symbol}: {e}')
        return pd.DataFrame()

# Function to get insider sentiment
def get_insider_sentiment(symbol, from_date, to_date):
    if not symbol:
        return pd.DataFrame()
    try:
        sentiment = finnhub_client.stock_insider_sentiment(symbol, from_date, to_date)
        if sentiment and 'data' in sentiment:
            df = pd.DataFrame(sentiment['data'])
            if 'year' in df.columns:
                df['year'] = df['year'].astype(str).str.replace(',','')
                
            st.write("Insider Sentiment:", df)
            return df
        else:
            st.error(f'No insider sentiment data found for {symbol}.')
            return pd.DataFrame()
    except Exception as e:
        st.error(f'An error occurred fetching insider sentiment for {symbol}: {e}')
        return pd.DataFrame()

# Streamlit layout
st.title('Insider Transactions and Sentiment')
symbol = st.text_input('Enter a stock symbol e.g: AAPL', 'AAPL')

# Get the date range input from the last 6 months to today
from_date = st.date_input('From date', pd.to_datetime('today') - pd.DateOffset(months=12))
to_date = st.date_input('To date', pd.to_datetime('today'))

# Button to fetch insider transactions
if st.button('Get Insider Data'):
    if symbol:
        get_insider_transactions(symbol, from_date, to_date)
        get_insider_sentiment(symbol, from_date, to_date)
    else:
        st.warning('Please enter a stock symbol to get insider data.')

