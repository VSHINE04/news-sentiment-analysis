"""
Setup Test Script
Verifies that all components are properly installed and configured
"""

import sys
from importlib import import_module

def test_python_version():
    """Test Python version"""
    print("\n" + "="*60)
    print("Testing Python Version")
    print("="*60)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def test_package(package_name, display_name=None):
    """Test if a package is installed"""
    if display_name is None:
        display_name = package_name
    
    try:
        module = import_module(package_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {display_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {display_name}: Not installed")
        return False

def test_packages():
    """Test all required packages"""
    print("\n" + "="*60)
    print("Testing Required Packages")
    print("="*60)
    
    packages = [
        ('pyspark', 'PySpark'),
        ('pymongo', 'PyMongo'),
        ('newsapi', 'NewsAPI'),
        ('pandas', 'Pandas'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
        ('textblob', 'TextBlob'),
        ('vaderSentiment', 'VADER Sentiment'),
        ('streamlit', 'Streamlit'),
        ('plotly', 'Plotly'),
        ('dotenv', 'Python-dotenv')
    ]
    
    results = []
    for package, display in packages:
        results.append(test_package(package, display))
    
    return all(results)

def test_configuration():
    """Test configuration file"""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)
    
    try:
        import config
        
        # Check API key
        if config.NEWS_API_KEY:
            print(f"✅ NewsAPI Key: Set ({config.NEWS_API_KEY[:10]}...)")
        else:
            print("❌ NewsAPI Key: Not set")
            return False
        
        # Check MongoDB URI
        if config.MONGODB_URI:
            print(f"✅ MongoDB URI: Set")
        else:
            print("❌ MongoDB URI: Not set")
            return False
        
        # Check other settings
        print(f"✅ Database: {config.MONGODB_DB}")
        print(f"✅ Collection: {config.MONGODB_COLLECTION}")
        print(f"✅ Spark Master: {config.SPARK_MASTER}")
        
        return True
    
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n" + "="*60)
    print("Testing MongoDB Connection")
    print("="*60)
    
    try:
        from mongodb_handler import MongoDBHandler
        
        handler = MongoDBHandler()
        print("✅ MongoDB connection successful")
        
        # Test basic operation
        stats = handler.get_statistics()
        print(f"✅ Database accessible: {stats.get('total_articles', 0)} articles")
        
        handler.close()
        return True
    
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        return False

def test_spark():
    """Test Spark initialization"""
    print("\n" + "="*60)
    print("Testing Apache Spark")
    print("="*60)
    
    try:
        from sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        print("✅ Spark session created successfully")
        
        # Test basic operation
        test_data = [{
            'title': 'Test',
            'description': 'Test article',
            'full_text': 'Test article',
            'source': 'Test',
            'author': 'Test'
        }]
        
        result = analyzer.analyze_articles(test_data)
        
        if result is not None:
            print("✅ Spark analysis working")
            analyzer.stop()
            return True
        else:
            print("❌ Spark analysis failed")
            analyzer.stop()
            return False
    
    except Exception as e:
        print(f"❌ Spark initialization failed: {str(e)}")
        return False

def test_visualization():
    """Test visualization capabilities"""
    print("\n" + "="*60)
    print("Testing Visualization")
    print("="*60)
    
    try:
        from visualizer import Visualizer
        import pandas as pd
        
        viz = Visualizer()
        print("✅ Visualizer initialized")
        
        # Create test data
        test_data = pd.DataFrame({
            'sentiment': ['Positive', 'Negative', 'Neutral'] * 3,
            'sentiment_score': [0.5, -0.5, 0.0] * 3,
            'source': ['Test'] * 9,
            'published_at': pd.date_range('2024-01-01', periods=9)
        })
        
        # Test one plot
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend for testing
        
        result = viz.plot_sentiment_distribution(test_data, save=False)
        print("✅ Visualization working")
        
        return True
    
    except Exception as e:
        print(f"❌ Visualization failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("NEWS SENTIMENT ANALYSIS - SETUP TEST")
    print("="*70)
    
    results = {
        'Python Version': test_python_version(),
        'Required Packages': test_packages(),
        'Configuration': test_configuration(),
        'MongoDB Connection': test_mongodb_connection(),
        'Apache Spark': test_spark(),
        'Visualization': test_visualization()
    }
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test:.<50} {status}")
    
    print("="*70)
    
    if all(results.values()):
        print("\n✅ ALL TESTS PASSED! System is ready to use.")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)
