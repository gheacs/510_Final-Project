import finnhub
import streamlit as st
import pandas as pd

# Initialize Finnhub client with your API key
api_key = 'cnn42hhr01qq36n5lak0cnn42hhr01qq36n5lakg'  # Use your actual Finnhub API key
finnhub_client = finnhub.Client(api_key=api_key)

# Function to get company news
def get_company_news(symbol, from_date, to_date):
    if not symbol:
        st.error('No symbol provided for fetching news.')
        return []
    try:
        news = finnhub_client.company_news(symbol, _from=from_date, to=to_date)
        if news:
            return news
        else:
            st.error(f'No news found for {symbol}.')
            return []
    except Exception as e:
        st.error(f'An error occurred fetching news for {symbol}: {e}')
        return []

# Streamlit layout
st.title('Company News and Insider Transactions')
symbol = st.text_input('Enter a stock symbol, e.g., AAPL', 'AAPL')

from_date = st.date_input('From date', value=pd.to_datetime('today') - pd.DateOffset(years=1))
to_date = st.date_input('To date', value=pd.to_datetime('today'))

if st.button('Get Company News'):
    news_data = get_company_news(symbol, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
    if news_data:
        for article in news_data:
            st.subheader(article['headline'])
            st.write(article['summary'])

            # Check if the image URL is valid before trying to display it
            if article.get('image'):  # Using .get to avoid KeyError if 'image' key doesn't exist
                try:
                    st.image(article['image'], use_column_width=True)
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            
            st.write(f"Read more: [link]({article['url']})")
            st.write('---')
