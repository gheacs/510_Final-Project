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

# Function to get stories for specific companies
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

    print(f"Total number of stories fetched for tickers {tickers}: {len(all_stories)}")
    return all_stories

# Save data to CSV file
def save_data_to_csv(stories, file_name='aylien_news_stories.csv'):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Article ID', 'Title', 'Published At', 'Summary', 'Entity ID', 'Entity Text',
            'Stock Tickers', 'Sentiment Polarity', 'Sentiment Confidence', 'Category ID', 'Category Label', 
            'Keywords', 'Article URL'
        ])

        for story in stories:
            article_id = story.get('id', 'N/A')
            title = story.get('title', 'No Title')
            published_at = story.get('published_at', 'N/A')
            summary = story.get('summary', {}).get('sentences', [])
            summary_text = ' '.join(summary)
            permalink = story.get('links', {}).get('permalink', 'N/A')
            keywords = ", ".join(story.get('keywords', []))

            sentiment = story.get('sentiment', {}).get('title', {})
            sentiment_polarity = sentiment.get('polarity', 'N/A')
            sentiment_confidence = story.get('sentiment', {}).get('body', {}).get('score', 'N/A')


            entities = story.get('entities', [])
            categories = story.get('categories', [])

            for entity in entities:
                entity_id = entity.get('id', 'N/A')
                entity_text = entity.get('text', 'N/A')
                stock_tickers = ", ".join(entity.get('stock_tickers', []))

                for category in categories:
                    category_id = category.get('id', 'N/A')
                    category_label = category.get('label', 'N/A')

                    writer.writerow([
                        article_id, title, published_at, summary_text, entity_id, entity_text,
                        stock_tickers, sentiment_polarity, sentiment_confidence, category_id, category_label, 
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
