"""
MongoDB Handler Module
Manages storage and retrieval of news articles with sentiment analysis results
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
import pandas as pd
import config

class MongoDBHandler:
    """Handles MongoDB operations for news sentiment data"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        if not config.MONGODB_URI:
            raise ValueError("MONGODB_URI not configured. Please set it in .env file")
        
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            print("🔌 Connecting to MongoDB...")
            self.client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database and collection
            self.db = self.client[config.MONGODB_DB]
            self.collection = self.db[config.MONGODB_COLLECTION]
            
            print(f"✅ Connected to MongoDB: {config.MONGODB_DB}.{config.MONGODB_COLLECTION}")
        
        except ConnectionFailure as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            raise
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {str(e)}")
            raise
    
    def insert_articles(self, df):
        """
        Insert analyzed articles into MongoDB
        
        Args:
            df (DataFrame): Spark or Pandas DataFrame with articles
        
        Returns:
            int: Number of articles inserted
        """
        try:
            # Convert Spark DataFrame to Pandas if needed
            if hasattr(df, 'toPandas'):
                pdf = df.toPandas()
            else:
                pdf = df
            
            # Convert to dictionary records
            records = pdf.to_dict('records')
            
            if not records:
                print("⚠️ No records to insert")
                return 0
            
            # Add insertion timestamp
            for record in records:
                record['inserted_at'] = datetime.now()
                
                # Convert numpy types to Python types
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                        record[key] = value.to_pydatetime() if hasattr(value, 'to_pydatetime') else str(value)
            
            # Insert documents
            result = self.collection.insert_many(records)
            inserted_count = len(result.inserted_ids)
            
            print(f"✅ Inserted {inserted_count} articles into MongoDB")
            return inserted_count
        
        except Exception as e:
            print(f"❌ Error inserting articles: {str(e)}")
            return 0
    
    def get_all_articles(self, limit=1000):
        """
        Retrieve all articles from MongoDB
        
        Args:
            limit (int): Maximum number of articles to retrieve
        
        Returns:
            list: List of article dictionaries
        """
        try:
            # Convert ObjectId to string for Spark compatibility
            articles = []
            cursor = self.collection.find().limit(limit)
            
            for article in cursor:
                article['_id'] = str(article['_id'])
                articles.append(article)
            
            print(f"✅ Retrieved {len(articles)} articles from MongoDB")
            return articles
        
        except Exception as e:
            print(f"❌ Error retrieving articles: {str(e)}")
            return []
    
    def get_articles_by_sentiment(self, sentiment, limit=100):
        """
        Retrieve articles filtered by sentiment
        
        Args:
            sentiment (str): Sentiment label (Positive, Neutral, Negative)
            limit (int): Maximum number of articles
        
        Returns:
            list: List of article dictionaries
        """
        try:
            articles = []
            cursor = self.collection.find({'sentiment': sentiment}).limit(limit)
            
            for article in cursor:
                article['_id'] = str(article['_id'])
                articles.append(article)
            
            print(f"✅ Retrieved {len(articles)} {sentiment} articles")
            return articles
        
        except Exception as e:
            print(f"❌ Error retrieving articles: {str(e)}")
            return []
    
    def get_articles_by_source(self, source, limit=100):
        """
        Retrieve articles from a specific source
        
        Args:
            source (str): Source name
            limit (int): Maximum number of articles
        
        Returns:
            list: List of article dictionaries
        """
        try:
            articles = []
            cursor = self.collection.find({'source': source}).limit(limit)
            
            for article in cursor:
                article['_id'] = str(article['_id'])
                articles.append(article)
            
            print(f"✅ Retrieved {len(articles)} articles from {source}")
            return articles
        
        except Exception as e:
            print(f"❌ Error retrieving articles: {str(e)}")
            return []
    
    def get_statistics(self):
        """
        Get comprehensive statistics about stored articles
        
        Returns:
            dict: Statistics dictionary
        """
        try:
            total = self.collection.count_documents({})
            
            if total == 0:
                print("⚠️ No articles in database")
                return {}
            
            # Sentiment distribution
            positive = self.collection.count_documents({'sentiment': 'Positive'})
            neutral = self.collection.count_documents({'sentiment': 'Neutral'})
            negative = self.collection.count_documents({'sentiment': 'Negative'})
            
            # Average scores
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'avg_sentiment_score': {'$avg': '$sentiment_score'},
                        'avg_vader': {'$avg': '$vader_compound'},
                        'avg_textblob': {'$avg': '$textblob_polarity'}
                    }
                }
            ]
            
            avg_result = list(self.collection.aggregate(pipeline))
            avg_scores = avg_result[0] if avg_result else {}
            
            # Top sources
            source_pipeline = [
                {'$group': {'_id': '$source', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            
            top_sources = list(self.collection.aggregate(source_pipeline))
            
            # Date range
            date_pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'oldest': {'$min': '$published_at'},
                        'newest': {'$max': '$published_at'}
                    }
                }
            ]
            
            date_result = list(self.collection.aggregate(date_pipeline))
            date_range = date_result[0] if date_result else {}
            
            stats = {
                'total_articles': total,
                'positive_count': positive,
                'neutral_count': neutral,
                'negative_count': negative,
                'positive_percentage': (positive / total * 100) if total > 0 else 0,
                'neutral_percentage': (neutral / total * 100) if total > 0 else 0,
                'negative_percentage': (negative / total * 100) if total > 0 else 0,
                'avg_sentiment_score': avg_scores.get('avg_sentiment_score', 0),
                'avg_vader_score': avg_scores.get('avg_vader', 0),
                'avg_textblob_score': avg_scores.get('avg_textblob', 0),
                'top_sources': top_sources,
                'oldest_article': date_range.get('oldest', 'N/A'),
                'newest_article': date_range.get('newest', 'N/A')
            }
            
            return stats
        
        except Exception as e:
            print(f"❌ Error getting statistics: {str(e)}")
            return {}
    
    def print_statistics(self, stats=None):
        """Print database statistics"""
        if stats is None:
            stats = self.get_statistics()
        
        if not stats:
            print("⚠️ No statistics available")
            return
        
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        print(f"Total Articles: {stats['total_articles']}")
        print(f"\nSentiment Distribution:")
        print(f"  Positive: {stats['positive_count']} ({stats['positive_percentage']:.1f}%)")
        print(f"  Neutral:  {stats['neutral_count']} ({stats['neutral_percentage']:.1f}%)")
        print(f"  Negative: {stats['negative_count']} ({stats['negative_percentage']:.1f}%)")
        print(f"\nAverage Scores:")
        print(f"  Overall:  {stats['avg_sentiment_score']:.3f}")
        print(f"  VADER:    {stats['avg_vader_score']:.3f}")
        print(f"  TextBlob: {stats['avg_textblob_score']:.3f}")
        
        if stats.get('top_sources'):
            print(f"\nTop Sources:")
            for i, source in enumerate(stats['top_sources'][:5], 1):
                print(f"  {i}. {source['_id']}: {source['count']} articles")
        
        print(f"\nDate Range:")
        print(f"  Oldest: {stats['oldest_article']}")
        print(f"  Newest: {stats['newest_article']}")
        print("="*60 + "\n")
    
    def delete_all_articles(self):
        """Delete all articles from collection (use with caution!)"""
        try:
            result = self.collection.delete_many({})
            print(f"✅ Deleted {result.deleted_count} articles")
            return result.deleted_count
        except Exception as e:
            print(f"❌ Error deleting articles: {str(e)}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")

# Example usage
if __name__ == "__main__":
    # Test the handler
    handler = MongoDBHandler()
    
    # Get statistics
    handler.print_statistics()
    
    # Close connection
    handler.close()
