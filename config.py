"""
Configuration Management for News Sentiment Analysis
Loads settings from environment variables and provides defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# NewsAPI Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_BASE_URL = 'https://newsapi.org/v2'
NEWS_API_PAGE_SIZE = 100  # Max articles per request
NEWS_API_LANGUAGE = 'en'  # English articles

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB = os.getenv('MONGODB_DB', 'news_sentiment_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'news_articles')

# Spark Configuration
SPARK_APP_NAME = "NewsSentimentAnalysis"
SPARK_MASTER = "local[1]"  # Use single thread for Windows compatibility
SPARK_DRIVER_MEMORY = "2g"
SPARK_EXECUTOR_MEMORY = "2g"
SPARK_PARTITIONS = 1

# Sentiment Analysis Configuration
SENTIMENT_POSITIVE_THRESHOLD = 0.05
SENTIMENT_NEGATIVE_THRESHOLD = -0.05

# Visualization Configuration
OUTPUT_DIR = "output"
CHART_STYLE = "seaborn-v0_8-darkgrid"
FIGURE_SIZE = (12, 6)

# Dashboard Configuration
DASHBOARD_PORT = 8501
DASHBOARD_REFRESH_INTERVAL = 300  # 5 minutes in seconds

# Categories for NewsAPI
NEWS_CATEGORIES = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]

def validate_config():
    """Validate that required configuration variables are set"""
    errors = []
    
    if not NEWS_API_KEY:
        errors.append("NEWS_API_KEY not found in .env file")
    
    if not MONGODB_URI:
        errors.append("MONGODB_URI not found in .env file")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ Configuration validated successfully")
    return True

def create_output_directory():
    """Create output directory for visualizations if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✅ Created output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    print("=== News Sentiment Analysis Configuration ===")
    print(f"NewsAPI Key: {'✓ Set' if NEWS_API_KEY else '✗ Not Set'}")
    print(f"MongoDB URI: {'✓ Set' if MONGODB_URI else '✗ Not Set'}")
    print(f"Database: {MONGODB_DB}")
    print(f"Collection: {MONGODB_COLLECTION}")
    print(f"Spark Master: {SPARK_MASTER}")
    print(f"Output Directory: {OUTPUT_DIR}")
    validate_config()
