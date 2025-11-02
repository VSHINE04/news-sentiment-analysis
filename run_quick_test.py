"""
Quick Test Script
Runs a quick end-to-end test of the sentiment analysis pipeline
"""

import sys
from datetime import datetime

def quick_test():
    """Run quick end-to-end test"""
    print("\n" + "="*70)
    print("NEWS SENTIMENT ANALYSIS - QUICK TEST")
    print("="*70)
    
    # Test 1: Import modules
    print("\n📦 Test 1: Importing modules...")
    try:
        import config
        from news_collector import NewsCollector
        from sentiment_analyzer import SentimentAnalyzer
        from mongodb_handler import MongoDBHandler
        from visualizer import Visualizer
        print("✅ All modules imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False
    
    # Test 2: Configuration
    print("\n⚙️  Test 2: Checking configuration...")
    try:
        if not config.validate_config():
            print("❌ Configuration validation failed")
            return False
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False
    
    # Test 3: Sample sentiment analysis
    print("\n🔍 Test 3: Running sample sentiment analysis...")
    try:
        analyzer = SentimentAnalyzer()
        
        # Sample articles
        test_articles = [
            {
                'title': 'Amazing breakthrough in AI technology',
                'description': 'Scientists achieve remarkable progress in artificial intelligence',
                'full_text': 'Amazing breakthrough in AI technology. Scientists achieve remarkable progress in artificial intelligence',
                'source': 'TechNews',
                'author': 'John Doe',
                'published_at': datetime.now().isoformat(),
                'url': 'https://example.com/1'
            },
            {
                'title': 'Economic crisis deepens',
                'description': 'Markets plunge amid growing concerns',
                'full_text': 'Economic crisis deepens. Markets plunge amid growing concerns',
                'source': 'FinanceNews',
                'author': 'Jane Smith',
                'published_at': datetime.now().isoformat(),
                'url': 'https://example.com/2'
            },
            {
                'title': 'Weather update for tomorrow',
                'description': 'Partly cloudy with moderate temperatures expected',
                'full_text': 'Weather update for tomorrow. Partly cloudy with moderate temperatures expected',
                'source': 'WeatherChannel',
                'author': 'Bob Johnson',
                'published_at': datetime.now().isoformat(),
                'url': 'https://example.com/3'
            }
        ]
        
        # Analyze
        result_df = analyzer.analyze_articles(test_articles)
        
        if result_df is None:
            print("❌ Analysis failed")
            analyzer.stop()
            return False
        
        # Get summary
        summary = analyzer.get_sentiment_summary(result_df)
        
        print("✅ Sentiment analysis completed")
        print(f"   - Positive: {summary['positive_count']}")
        print(f"   - Neutral: {summary['neutral_count']}")
        print(f"   - Negative: {summary['negative_count']}")

        # Convert to pandas BEFORE stopping Spark to avoid context errors downstream
        pdf_results = result_df.toPandas() if hasattr(result_df, 'toPandas') else result_df

        analyzer.stop()
    
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: MongoDB connection
    print("\n💾 Test 4: Testing MongoDB connection...")
    try:
        db_handler = MongoDBHandler()
        stats = db_handler.get_statistics()
        print(f"✅ MongoDB connected (Total articles: {stats.get('total_articles', 0)})")
        db_handler.close()
    except Exception as e:
        print(f"❌ MongoDB error: {str(e)}")
        return False
    
    # Test 5: Visualization
    print("\n📊 Test 5: Testing visualization...")
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        
        viz = Visualizer()
        
        # Use pre-converted pandas DataFrame from analysis step
        pdf = pdf_results
        
        # Test one visualization
        viz.plot_sentiment_distribution(pdf, save=False)
        print("✅ Visualization working")
    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")
        return False
    
    return True

def main():
    """Main function"""
    try:
        success = quick_test()
        
        print("\n" + "="*70)
        if success:
            print("✅ ALL QUICK TESTS PASSED!")
            print("\n🚀 System is ready to use!")
            print("\nNext steps:")
            print("  1. Run: python main.py")
            print("  2. Or use: run.bat (Windows CMD)")
            print("  3. Or use: run.ps1 (PowerShell)")
            print("  4. For dashboard: run_dashboard.bat")
        else:
            print("❌ SOME TESTS FAILED!")
            print("\n🔧 Please check the errors above and fix them.")
        print("="*70)
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)
