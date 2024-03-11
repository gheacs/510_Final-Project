import streamlit as st
import requests

# Define your Aylien credentials
AppID = '099aea53'  # Your Application ID
APIKey = '52a907255d173a6aa2a58755e9c7203c'  # Your API Key

# Function to get authentication header
def get_auth_header(appid, apikey):
    return {
        'X-Application-Id': appid,
        'X-Application-Key': apikey
    }

# Function to get stories
def get_stories(params, headers):
    fetched_stories = []
    base_url = 'https://api.aylien.com/news/stories'

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        fetched_stories = response.json().get('stories', [])
    else:
        st.error(f"Failed to fetch stories: {response.status_code} - {response.text}")

    return fetched_stories

# Streamlit app main function
def main():
    st.title('Aylien News Stories')

    # Setup headers with authentication
    headers = get_auth_header(AppID, APIKey)

    # Define parameters for the API call
    params = {
        'title': 'Apple',
        'published_at.start': 'NOW-60DAYS',
        'published_at.end': 'NOW',
        'cursor': '*',
        'per_page': 10,
        'language': 'en'
    }

    # Fetch stories from the API
    stories = get_stories(params, headers)

    # Display the stories in the Streamlit app
    for story in stories:
        st.header(story.get('title', 'No Title'))
        st.write(story.get('body', 'No Content'))

if __name__ == '__main__':
    main()
