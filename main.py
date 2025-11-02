"""
Main Application
News Sentiment Analysis Pipeline with Apache Spark
Menu-driven interface for complete ETL workflow
"""

import sys
from datetime import datetime, timedelta
import config
from news_collector import NewsCollector
from sentiment_analyzer import SentimentAnalyzer
from mongodb_handler import MongoDBHandler
from visualizer import Visualizer

class NewsSentimentApp:
    """Main application orchestrating the sentiment analysis pipeline"""
    
    def __init__(self):
        """Initialize application components"""
        print("\n" + "="*70)
        print("🚀 NEWS SENTIMENT ANALYSIS WITH APACHE SPARK")
        print("="*70 + "\n")
        
        # Validate configuration
        if not config.validate_config():
            print("\n❌ Please configure .env file with your API keys")
            sys.exit(1)
        
        # Initialize components
        self.collector = NewsCollector()
        self.analyzer = SentimentAnalyzer()
        self.db_handler = MongoDBHandler()
        self.visualizer = Visualizer()
        
        print("\n✅ All components initialized successfully\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("📋 MAIN MENU")
        print("="*70)
        print("1. Search news by keyword")
        print("2. Fetch top headlines by category")
        print("3. Analyze stored articles from database")
        print("4. View database statistics")
        print("5. Clear database (delete all articles)")
        print("6. Exit")
        print("="*70)
    
    def search_and_analyze(self):
        """Search news by keyword and perform complete analysis"""
        print("\n" + "="*70)
        print("🔍 SEARCH NEWS BY KEYWORD")
        print("="*70)
        
        # Get search parameters
        query = input("\nEnter search keyword (e.g., 'artificial intelligence'): ").strip()
        
        if not query:
            print("❌ Query cannot be empty")
            return
        
        try:
            days = int(input("Enter number of days to search (1-7, default 7): ").strip() or "7")
            days = min(max(days, 1), 7)  # Clamp between 1-7
        except ValueError:
            days = 7
        
        try:
            max_articles = int(input("Enter max articles to fetch (1-100, default 50): ").strip() or "50")
            max_articles = min(max(max_articles, 1), 100)  # Clamp between 1-100
        except ValueError:
            max_articles = 50
        
        # Calculate date range
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Fetch articles
        print(f"\n📡 Fetching articles about '{query}'...")
        articles = self.collector.fetch_everything(
            query=query,
            from_date=from_date,
            to_date=to_date,
            page_size=max_articles
        )
        
        if not articles:
            print("❌ No articles found")
            return
        
        # Analyze sentiment
        print(f"\n🔍 Analyzing sentiment with Spark...")
        result_df = self.analyzer.analyze_articles(articles)
        
        if result_df is None:
            print("❌ Analysis failed")
            return
        
        # Show summary
        summary = self.analyzer.get_sentiment_summary(result_df)
        self.analyzer.print_summary(summary)
        
        # Store in database
        save = input("💾 Save results to database? (y/n, default y): ").strip().lower()
        if save != 'n':
            self.db_handler.insert_articles(result_df)
        
        # Create visualizations
        visualize = input("📊 Create visualizations? (y/n, default y): ").strip().lower()
        if visualize != 'n':
            self.visualizer.create_all_plots(result_df)
    
    def fetch_headlines_and_analyze(self):
        """Fetch top headlines by category and analyze"""
        print("\n" + "="*70)
        print("📰 FETCH TOP HEADLINES")
        print("="*70)
        
        # Display categories
        print("\nAvailable categories:")
        for i, category in enumerate(config.NEWS_CATEGORIES, 1):
            print(f"{i}. {category.capitalize()}")
        
        try:
            choice = int(input(f"\nSelect category (1-{len(config.NEWS_CATEGORIES)}): ").strip())
            if 1 <= choice <= len(config.NEWS_CATEGORIES):
                category = config.NEWS_CATEGORIES[choice - 1]
            else:
                print("❌ Invalid choice")
                return
        except ValueError:
            print("❌ Invalid input")
            return
        
        try:
            max_articles = int(input("Enter max articles to fetch (1-100, default 50): ").strip() or "50")
            max_articles = min(max(max_articles, 1), 100)
        except ValueError:
            max_articles = 50
        
        # Fetch headlines
        print(f"\n📡 Fetching {category} headlines...")
        articles = self.collector.fetch_top_headlines(
            category=category,
            page_size=max_articles
        )
        
        if not articles:
            print("❌ No articles found")
            return
        
        # Analyze sentiment
        print(f"\n🔍 Analyzing sentiment with Spark...")
        result_df = self.analyzer.analyze_articles(articles)
        
        if result_df is None:
            print("❌ Analysis failed")
            return
        
        # Show summary
        summary = self.analyzer.get_sentiment_summary(result_df)
        self.analyzer.print_summary(summary)
        
        # Store in database
        save = input("💾 Save results to database? (y/n, default y): ").strip().lower()
        if save != 'n':
            self.db_handler.insert_articles(result_df)
        
        # Create visualizations
        visualize = input("📊 Create visualizations? (y/n, default y): ").strip().lower()
        if visualize != 'n':
            self.visualizer.create_all_plots(result_df)
    
    def analyze_stored_articles(self):
        """Analyze articles already stored in database"""
        print("\n" + "="*70)
        print("🔍 ANALYZE STORED ARTICLES")
        print("="*70)
        
        # Get articles from database
        print("\n📥 Retrieving articles from database...")
        articles = self.db_handler.get_all_articles(limit=1000)
        
        if not articles:
            print("❌ No articles in database")
            return
        
        # Create DataFrame
        import pandas as pd
        pdf = pd.DataFrame(articles)
        
        # Check if already analyzed
        if 'sentiment' in pdf.columns:
            print(f"✅ Found {len(articles)} analyzed articles")
            
            # Show summary
            summary = {
                'total_articles': len(pdf),
                'positive_count': len(pdf[pdf['sentiment'] == 'Positive']),
                'neutral_count': len(pdf[pdf['sentiment'] == 'Neutral']),
                'negative_count': len(pdf[pdf['sentiment'] == 'Negative']),
                'avg_sentiment_score': float(pdf['sentiment_score'].mean()) if 'sentiment_score' in pdf.columns else 0,
                'positive_percentage': (len(pdf[pdf['sentiment'] == 'Positive']) / len(pdf) * 100),
                'neutral_percentage': (len(pdf[pdf['sentiment'] == 'Neutral']) / len(pdf) * 100),
                'negative_percentage': (len(pdf[pdf['sentiment'] == 'Negative']) / len(pdf) * 100)
            }
            
            self.analyzer.print_summary(summary)
            
            # Create visualizations
            visualize = input("📊 Create visualizations? (y/n, default y): ").strip().lower()
            if visualize != 'n':
                self.visualizer.create_all_plots(pdf)
        else:
            print("⚠️ Articles not yet analyzed. Analyzing now...")
            
            # Analyze with Spark
            result_df = self.analyzer.analyze_articles(articles)
            
            if result_df is None:
                print("❌ Analysis failed")
                return
            
            # Show summary
            summary = self.analyzer.get_sentiment_summary(result_df)
            self.analyzer.print_summary(summary)
            
            # Update database
            update = input("💾 Update database with analysis results? (y/n, default y): ").strip().lower()
            if update != 'n':
                # This would require updating existing records
                print("⚠️ Database update not implemented. Consider re-running with save option.")
            
            # Create visualizations
            visualize = input("📊 Create visualizations? (y/n, default y): ").strip().lower()
            if visualize != 'n':
                self.visualizer.create_all_plots(result_df)
    
    def show_statistics(self):
        """Display database statistics"""
        print("\n" + "="*70)
        print("📊 DATABASE STATISTICS")
        print("="*70)
        
        self.db_handler.print_statistics()
    
    def clear_database(self):
        """Clear all articles from database"""
        print("\n" + "="*70)
        print("⚠️  CLEAR DATABASE")
        print("="*70)
        
        confirm = input("\n⚠️  This will delete ALL articles. Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.db_handler.delete_all_articles()
        else:
            print("❌ Operation cancelled")
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up resources...")
        self.analyzer.stop()
        self.db_handler.close()
        print("✅ Cleanup complete")
    
    def run(self):
        """Run the main application loop"""
        try:
            while True:
                self.display_menu()
                
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == '1':
                    self.search_and_analyze()
                elif choice == '2':
                    self.fetch_headlines_and_analyze()
                elif choice == '3':
                    self.analyze_stored_articles()
                elif choice == '4':
                    self.show_statistics()
                elif choice == '5':
                    self.clear_database()
                elif choice == '6':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid option. Please select 1-6.")
                
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

# Main entry point
if __name__ == "__main__":
    app = NewsSentimentApp()
    app.run()
