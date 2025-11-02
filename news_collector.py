"""
News Collector Module
Fetches news articles from NewsAPI with rate limiting and error handling
"""

import requests
from datetime import datetime, timedelta
import time
from newsapi import NewsApiClient
import config

class NewsCollector:
    """Collects news articles from NewsAPI"""
    
    def __init__(self):
        """Initialize NewsAPI client"""
        if not config.NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY not configured. Please set it in .env file")
        
        self.newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
        self.request_count = 0
        self.max_requests_per_day = 100  # Free tier limit
    
    def check_rate_limit(self):
        """Check if rate limit is reached"""
        if self.request_count >= self.max_requests_per_day:
            print(f"⚠️ Rate limit reached ({self.max_requests_per_day} requests/day)")
            return False
        return True
    
    def fetch_everything(self, query, from_date=None, to_date=None, page_size=100):
        """
        Fetch news articles based on a search query
        
        Args:
            query (str): Search query/keyword
            from_date (str): Start date (YYYY-MM-DD format)
            to_date (str): End date (YYYY-MM-DD format)
            page_size (int): Number of articles to fetch (max 100)
        
        Returns:
            list: List of article dictionaries
        """
        if not self.check_rate_limit():
            return []
        
        try:
            # Set default date range (last 7 days for free tier)
            if not to_date:
                to_date = datetime.now().strftime('%Y-%m-%d')
            if not from_date:
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            print(f"📡 Fetching articles for query: '{query}'")
            print(f"   Date range: {from_date} to {to_date}")
            
            # Fetch articles
            response = self.newsapi.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                language=config.NEWS_API_LANGUAGE,
                sort_by='publishedAt',
                page_size=page_size
            )
            
            self.request_count += 1
            
            if response['status'] == 'ok':
                articles = response.get('articles', [])
                print(f"✅ Fetched {len(articles)} articles")
                return self._clean_articles(articles)
            else:
                print(f"❌ API Error: {response.get('message', 'Unknown error')}")
                return []
        
        except Exception as e:
            print(f"❌ Error fetching articles: {str(e)}")
            return []
    
    def fetch_top_headlines(self, category=None, country='us', page_size=100):
        """
        Fetch top headlines by category
        
        Args:
            category (str): Category (business, entertainment, etc.)
            country (str): Country code (us, gb, etc.)
            page_size (int): Number of articles to fetch (max 100)
        
        Returns:
            list: List of article dictionaries
        """
        if not self.check_rate_limit():
            return []
        
        try:
            print(f"📡 Fetching top headlines")
            if category:
                print(f"   Category: {category}")
            
            # Fetch headlines
            response = self.newsapi.get_top_headlines(
                category=category,
                country=country,
                page_size=page_size
            )
            
            self.request_count += 1
            
            if response['status'] == 'ok':
                articles = response.get('articles', [])
                print(f"✅ Fetched {len(articles)} headlines")
                return self._clean_articles(articles)
            else:
                print(f"❌ API Error: {response.get('message', 'Unknown error')}")
                return []
        
        except Exception as e:
            print(f"❌ Error fetching headlines: {str(e)}")
            return []
    
    def _clean_articles(self, articles):
        """
        Clean and standardize article data
        
        Args:
            articles (list): Raw articles from API
        
        Returns:
            list: Cleaned article dictionaries
        """
        cleaned_articles = []
        
        for article in articles:
            # Skip articles with missing essential data
            if not article.get('title') or not article.get('description'):
                continue
            
            cleaned_article = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('content', ''),
                'author': article.get('author', 'Unknown'),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'fetched_at': datetime.now().isoformat()
            }
            
            # Combine title and description for analysis
            cleaned_article['full_text'] = f"{cleaned_article['title']}. {cleaned_article['description']}"
            
            cleaned_articles.append(cleaned_article)
        
        return cleaned_articles
    
    def get_sources(self, category=None, language='en'):
        """
        Get available news sources
        
        Args:
            category (str): Filter by category
            language (str): Filter by language
        
        Returns:
            list: List of source dictionaries
        """
        try:
            response = self.newsapi.get_sources(
                category=category,
                language=language
            )
            
            if response['status'] == 'ok':
                sources = response.get('sources', [])
                print(f"✅ Found {len(sources)} sources")
                return sources
            else:
                print(f"❌ API Error: {response.get('message', 'Unknown error')}")
                return []
        
        except Exception as e:
            print(f"❌ Error fetching sources: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    # Test the collector
    collector = NewsCollector()
    
    # Fetch articles about "artificial intelligence"
    articles = collector.fetch_everything("artificial intelligence", page_size=10)
    
    if articles:
        print(f"\n📰 Sample Article:")
        article = articles[0]
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published: {article['published_at']}")
        print(f"Description: {article['description'][:100]}...")
