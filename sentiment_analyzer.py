"""
Sentiment Analyzer Module
Pure Pandas implementation using VADER + TextBlob for sentiment analysis
"""

import os
import sys
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import config

# Simple lexicon arrays for Spark array operations
POSITIVE_WORDS = ["good","great","excellent","amazing","positive","fortunate","correct","superior",
                 "success","win","growth","improve","improved","improving","innovation","happy","benefit",
                 "best","strong","optimistic","gain","surge","record","beat","bullish"]

NEGATIVE_WORDS = ["bad","terrible","poor","awful","negative","unfortunate","wrong","inferior",
                 "loss","lose","decline","drop","dropped","fall","fallen","crash","panic","fear",
                 "worst","weak","pessimistic","bearish","risk","lawsuit","fraud","scandal"]



class SentimentAnalyzer:
    """Pandas-based sentiment analyzer using VADER + TextBlob."""

    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        print("✅ Sentiment Analyzer initialized (Pandas Mode - VADER + TextBlob)")

    def analyze_articles(self, articles: list):
        """Analyze articles using VADER + TextBlob sentiment analysis."""
        if not articles:
            print("⚠️ No articles to analyze")
            return None

        print(f"🔍 Analyzing {len(articles)} articles with VADER + TextBlob...")
        
        # Create DataFrame
        df = pd.DataFrame(articles)

        # Build combined text field
        for col in ["title", "description", "content", "full_text"]:
            if col not in df.columns:
                df[col] = ""
        
        df["full_text"] = df[["title", "description", "content", "full_text"]].fillna("").astype(str).agg(". ".join, axis=1)

        # Clean text
        df["cleaned_text"] = (
            df["full_text"].str.lower()
            .str.replace(r"http\S+|www\S+|https\S+", "", regex=True)
            .str.replace(r"<.*?>", "", regex=True)
            .str.replace(r"[^\w\s!?.,]", "", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        # Calculate sentiment scores
        def get_vader_score(text):
            """Get VADER compound score."""
            return self.vader_analyzer.polarity_scores(text).get("compound", 0.0)
        
        def get_textblob_score(text):
            """Get TextBlob polarity score."""
            return TextBlob(text).sentiment.polarity

        df["vader_compound"] = df["cleaned_text"].apply(get_vader_score)
        df["textblob_polarity"] = df["cleaned_text"].apply(get_textblob_score)
        
        # Average the two scores
        df["sentiment_score"] = (df["vader_compound"] + df["textblob_polarity"]) / 2.0

        # Classify sentiment based on thresholds
        pos_threshold = float(config.SENTIMENT_POSITIVE_THRESHOLD)
        neg_threshold = float(config.SENTIMENT_NEGATIVE_THRESHOLD)
        
        def classify_sentiment(score):
            if score >= pos_threshold:
                return "Positive"
            elif score <= neg_threshold:
                return "Negative"
            else:
                return "Neutral"
        
        df["sentiment"] = df["sentiment_score"].apply(classify_sentiment)
        
        print("✅ Sentiment analysis completed")
        return df

    def get_sentiment_summary(self, df):
        """Get summary statistics from analyzed DataFrame."""
        if df is None or df.empty:
            return {}

        total = len(df)
        pos = len(df[df["sentiment"] == "Positive"])
        neu = len(df[df["sentiment"] == "Neutral"])
        neg = len(df[df["sentiment"] == "Negative"])

        return {
            "total_articles": total,
            "positive_count": pos,
            "neutral_count": neu,
            "negative_count": neg,
            "positive_percentage": (pos / total * 100) if total > 0 else 0.0,
            "neutral_percentage": (neu / total * 100) if total > 0 else 0.0,
            "negative_percentage": (neg / total * 100) if total > 0 else 0.0,
            "avg_vader_score": float(df["vader_compound"].mean()) if "vader_compound" in df.columns else 0.0,
            "avg_textblob_score": float(df["textblob_polarity"].mean()) if "textblob_polarity" in df.columns else 0.0,
            "avg_sentiment_score": float(df["sentiment_score"].mean()) if "sentiment_score" in df.columns else 0.0,
        }

    def print_summary(self, summary):
        """Print sentiment analysis summary."""
        if not summary:
            return
        print("\n" + "=" * 60)
        print("📊 SENTIMENT ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Total Articles: {summary['total_articles']}")
        print("\nSentiment Distribution:")
        print(f"  ✅ Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
        print(f"  ⚪ Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
        print(f"  ❌ Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")
        print("\nAverage Scores:")
        print(f"  VADER:    {summary['avg_vader_score']:7.3f}")
        print(f"  TextBlob: {summary['avg_textblob_score']:7.3f}")
        print(f"  Overall:  {summary['avg_sentiment_score']:7.3f}")
        print("=" * 60 + "\n")

    def stop(self):
        """Cleanup resources."""
        pass  # No resources to cleanup with pure Pandas


# Example usage
if __name__ == "__main__":
    # Test the analyzer
    analyzer = SentimentAnalyzer()
    
    # Sample articles
    test_articles = [
        {
            'title': 'Amazing breakthrough in AI technology',
            'description': 'Scientists make incredible progress',
            'full_text': 'Amazing breakthrough in AI technology. Scientists make incredible progress',
            'source': 'TechNews',
            'author': 'John Doe'
        },
        {
            'title': 'Stock market crash causes panic',
            'description': 'Investors lose millions in devastating crash',
            'full_text': 'Stock market crash causes panic. Investors lose millions in devastating crash',
            'source': 'FinanceNews',
            'author': 'Jane Smith'
        },
        {
            'title': 'Weather forecast shows sunny skies',
            'description': 'Nice weather expected tomorrow',
            'full_text': 'Weather forecast shows sunny skies. Nice weather expected tomorrow',
            'source': 'WeatherChannel',
            'author': 'Bob Weather'
        }
    ]
    
    # Analyze
    result_df = analyzer.analyze_articles(test_articles)
    
    if result_df is not None:
        # Get summary
        summary = analyzer.get_sentiment_summary(result_df)
        analyzer.print_summary(summary)
        
        # Show detailed results
        print("📄 Detailed Results:")
        print(result_df[["title", "sentiment", "sentiment_score", "vader_compound", "textblob_polarity"]].to_string())
        analyzer.stop()

