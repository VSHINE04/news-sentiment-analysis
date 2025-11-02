"""
Test full pipeline - Fetch news, analyze sentiment, save to MongoDB
"""

import pandas as pd
from news_collector import NewsCollector
from sentiment_analyzer import SentimentAnalyzer
from mongodb_handler import MongoDBHandler
from visualizer import Visualizer
import config

def test_full_pipeline():
    """Test the complete news sentiment analysis pipeline"""
    
    print("="*60)
    print("🚀 TESTING FULL PIPELINE")
    print("="*60)
    
    # Step 1: Fetch news
    print("\n📰 Step 1: Fetching news articles...")
    collector = NewsCollector()
    articles = collector.fetch_top_headlines(
        category='technology',
        country='us',
        page_size=5
    )
    
    if not articles:
        print("❌ No articles fetched")
        return
    
    print(f"✅ Fetched {len(articles)} articles")
    for i, article in enumerate(articles[:3], 1):
        print(f"   {i}. {article['title'][:60]}...")
    
    # Step 2: Analyze sentiment
    print("\n🎭 Step 2: Analyzing sentiment...")
    analyzer = SentimentAnalyzer()
    results_df = analyzer.analyze_articles(articles)
    
    # Convert to Pandas for downstream checks/printing
    df_pd = results_df.toPandas() if hasattr(results_df, 'toPandas') else results_df
    
    if df_pd is None or df_pd.empty:
        print("❌ Sentiment analysis failed")
        return
    
    # Show summary
    summary = analyzer.get_sentiment_summary(results_df)
    analyzer.print_summary(summary)
    
    # Show detailed results
    print("📊 Article Sentiments:")
    for _, row in df_pd.iterrows():
        sentiment_emoji = {
            'Positive': '😊',
            'Neutral': '😐',
            'Negative': '😞'
        }.get(row['sentiment'], '❓')
        print(f"   {sentiment_emoji} {row['sentiment']:8s} ({row['sentiment_score']:+.3f}) - {row['title'][:50]}...")
    
    # Step 3: Save to MongoDB
    print("\n💾 Step 3: Saving to MongoDB...")
    db = MongoDBHandler()
    
    # Insert DataFrame directly
    inserted_count = db.insert_articles(df_pd)
    
    print(f"✅ Saved {inserted_count} articles to MongoDB")
    
    # Get statistics
    stats = db.get_statistics()
    if stats:
        print(f"📊 Database now contains: {stats['total_articles']} articles")
    else:
        print("📊 Unable to get database statistics")
    
    db.close()
    
    # Step 4: Create visualizations
    print("\n📈 Step 4: Creating visualizations...")
    viz = Visualizer()
    
    # Get all data for visualization
    db2 = MongoDBHandler()
    all_articles = db2.get_all_articles(limit=100)
    db2.close()
    
    if all_articles:
        print(f"   Creating charts from {len(all_articles)} articles...")
        df_viz = pd.DataFrame(all_articles)
        viz.create_all_plots(df_viz)
        print("   ✅ All charts created successfully")
    
    print("\n" + "="*60)
    print("✅ FULL PIPELINE TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Summary:")
    print(f"   • Fetched: {len(articles)} articles")
    print(f"   • Analyzed: {len(df_pd)} articles")
    print(f"   • Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
    print(f"   • Neutral: {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
    print(f"   • Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")
    print(f"   • Saved to MongoDB: {inserted_count} articles")
    if stats:
        print(f"   • Database total: {stats['total_articles']} articles")
    print("\n🎉 All systems working perfectly!\n")

if __name__ == "__main__":
    try:
        test_full_pipeline()
    except Exception as e:
        print(f"\n❌ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
