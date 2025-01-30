import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os


def load_existing_articles():
    try:
        if os.path.exists('forbes_articles_innovation.json'):
            with open('forbes_articles_innovation.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except json.JSONDecodeError:
        print("Error reading articles file, starting fresh")
        return []


def save_articles(articles):
    with open('forbes_articles_innovation.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)


def scrape_forbes():
    url = 'https://www.forbes.com/innovation'  # You can change this to other Forbes sections

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1'
    }

    existing_articles = load_existing_articles()
    existing_titles = {article['title'] for article in existing_articles}
    new_articles_found = False

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Using the exact class from the example
        article_links = soup.find_all('a', class_='_1-FLFW4R')

        for link in article_links:
            title = link.get_text(strip=True)
            url = link.get('href', '')

            if title and title not in existing_titles:
                # Create new article entry
                new_article = {
                    'title': title,
                    'url': url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                existing_articles.append(new_article)
                existing_titles.add(title)
                new_articles_found = True

                print(f'New article found: {title}')

        if new_articles_found:
            save_articles(existing_articles)
            print(f"Total articles saved: {len(existing_articles)}")

        return new_articles_found

    except requests.RequestException as e:
        print(f"Error making request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return False


def monitor_forbes_articles():
    print("Starting Forbes article monitor...")
    print("Press Ctrl+C to stop")

    while True:
        try:
            # Print current time
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\nChecking for new articles at {current_time}")

            # Scrape for new articles
            scrape_forbes()

            # Wait for 60 seconds
            print("\nWaiting 60 seconds before next check...", end='', flush=True)
            for _ in range(60):
                time.sleep(1)
                print('.', end='', flush=True)
            print('\n')

        except KeyboardInterrupt:
            print("\nStopping monitor...")
            break
        except Exception as e:
            print(f"An error occurred in the monitor loop: {e}")
            time.sleep(60)  # Wait before retrying


if __name__ == "__main__":
    # Print working directory information
    print(f"Working directory: {os.getcwd()}")
    print(f"Articles file will be saved to: {os.path.join(os.getcwd(), 'forbes_articles_innovation.json')}")

    monitor_forbes_articles()