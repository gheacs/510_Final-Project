import requests
import csv
from datetime import datetime, timedelta

# Define your Aylien credentials
AppID = '099aea53'  # Your Application ID
APIKey = '52a907255d173a6aa2a58755e9c7203c'  # Your API Key

# Function to get authentication header
def get_auth_header(appid, apikey):
    return {
        'X-Application-Id': appid,
        'X-Application-Key': apikey
    }

# Function to get stories for specific stock tickers
def get_stories_for_tickers(tickers, headers):
    all_stories = []
    base_url = 'https://api.aylien.com/news/stories'
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%dT%H:%M:%SZ')  # past 6 months
    end_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    for ticker in tickers:
        params = {
            'entities.stock_tickers': ticker,
            'published_at.start': start_date,
            'published_at.end': end_date,
            'language': 'en',
            'per_page': 100,
            'sort_by': 'published_at',
            'sort_direction': 'desc'
        }

        while True:
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                stories = data.get('stories', [])
                all_stories.extend(stories)

                if 'links' in data and 'next' in data['links']:
                    params['cursor'] = data['links']['next']
                else:
                    break
            else:
                print(f"Failed to fetch stories for ticker {ticker}: {response.status_code} - {response.text}")
                break

    return all_stories

# Save data to CSV file
def save_data_to_csv(stories, file_name='aylien_news_stories.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Article ID', 'Title', 'Published At', 'Summary', 'Sentences Count', 'Entity ID', 'Entity Text',
            'Stock Tickers', 'Body Sentiment Polarity', 'Body Sentiment Confidence', 
            'Title Sentiment Polarity', 'Title Sentiment Confidence', 'Category ID', 'Category Label', 
            'Keywords', 'Article URL'
        ])

        for story in stories:
            article_id = story.get('id', 'N/A')
            title = story.get('title', 'No Title')
            published_at = story.get('published_at', 'N/A')
            summary = story.get('summary', {}).get('sentences', [])
            summary_text = ' '.join(summary)
            sentences_count = story.get('sentences_count', 0)
            permalink = story.get('links', {}).get('permalink', 'N/A')
            keywords = ", ".join(story.get('keywords', []))

            body_sentiment = story.get('sentiment', {}).get('body', {})
            body_sentiment_polarity = body_sentiment.get('polarity', 'N/A')
            body_sentiment_confidence = body_sentiment.get('confidence', 'N/A')

            title_sentiment = story.get('sentiment', {}).get('title', {})
            title_sentiment_polarity = title_sentiment.get('polarity', 'N/A')
            title_sentiment_confidence = title_sentiment.get('confidence', 'N/A')

            entities = story.get('entities', [])
            categories = story.get('categories', [])

            entity_id = ', '.join([entity.get('id', 'N/A') for entity in entities])
            entity_text = ', '.join([entity.get('text', 'N/A') for entity in entities])
            stock_tickers = ', '.join([ticker for entity in entities for ticker in entity.get('stock_tickers', [])])

            category_id = ', '.join([category.get('id', 'N/A') for category in categories])
            category_label = ', '.join([category.get('label', 'N/A') for category in categories])

            writer.writerow([
                article_id, title, published_at, summary_text, sentences_count, entity_id, entity_text,
                stock_tickers, body_sentiment_polarity, body_sentiment_confidence,
                title_sentiment_polarity, title_sentiment_confidence, category_id, category_label, 
                keywords, permalink
            ])

    print(f"Data has been written to {file_name}")

def main():
    tickers = ['AAPL']
    headers = get_auth_header(AppID, APIKey)
    stories = get_stories_for_tickers(tickers, headers)
    save_data_to_csv(stories)

if __name__ == '__main__':
    main()
