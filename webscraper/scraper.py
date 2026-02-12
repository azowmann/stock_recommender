from ddgs import DDGS
from newspaper import Article, Config
import time

def search_articles(query, num_results=10):
    """
    Searches for articles using DuckDuckGo.
    """
    print(f"Searching for: {query}...")
    urls = []
    try:
        results = DDGS().text(query, max_results=num_results)
        # Convert to list to ensure we fetch them all and handle any generator issues
        results = list(results)
        for r in results:
            if 'href' in r:
                urls.append(r['href'])
    except Exception as e:
        print(f"Error during search: {e}")
    
    return urls

def download_article(url):
    """
    Downloads and parses a single article.
    """
    try:
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        config.request_timeout = 10
        
        article = Article(url, config=config)
        article.download()
        article.parse()
        # NLP is optional and slow
        # article.nlp() 
        
        return {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': str(article.publish_date) if article.publish_date else None,
            'url': url
        }
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def save_articles(articles, filename):
    """
    Saves the articles to a JSON file.
    """
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(articles)} articles to {filename}")
