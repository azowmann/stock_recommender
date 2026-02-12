import argparse
import os
import scraper
import nltk

def main():
    parser = argparse.ArgumentParser(description="Python Article Web Scraper")
    parser.add_argument("--keywords", type=str, required=True, help="Keywords to search for")
    parser.add_argument("--limit", type=int, default=5, help="Number of articles to download")
    parser.add_argument("--output", type=str, default="data/articles.json", help="Output JSON file path")

    args = parser.parse_args()

    # Ensure data directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # NLTK setup (safeguard)
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading necessary NLTK data...")
        nltk.download('punkt')
        nltk.download('punkt_tab') # Needed for newer nltk versions sometimes

    print(f"Searching for articles with keywords: '{args.keywords}'...")
    urls = scraper.search_articles(args.keywords, num_results=args.limit)
    
    if not urls:
        print("No articles found.")
        return

    print(f"Found {len(urls)} URLs. Starting download...")
    
    downloaded_articles = []
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Downloading: {url}")
        article_data = scraper.download_article(url)
        if article_data:
            downloaded_articles.append(article_data)
        else:
            print(f"Skipped {url}")

    if downloaded_articles:
        scraper.save_articles(downloaded_articles, args.output)
        print("Done!")
    else:
        print("No articles were successfully downloaded.")

if __name__ == "__main__":
    main()
