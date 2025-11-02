"""
Dashboard Application
Interactive Streamlit dashboard for news sentiment analysis
Real-time visualization with filters and auto-refresh
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import config
from mongodb_handler import MongoDBHandler

# Page configuration
st.set_page_config(
    page_title="News Sentiment Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_db_handler():
    """Initialize MongoDB handler (cached)"""
    return MongoDBHandler()

@st.cache_data(ttl=config.DASHBOARD_REFRESH_INTERVAL)
def load_data():
    """Load data from MongoDB (cached with TTL)"""
    db = get_db_handler()
    articles = db.get_all_articles(limit=1000)
    
    if not articles:
        return pd.DataFrame()
    
    df = pd.DataFrame(articles)
    
    # Convert dates
    if 'published_at' in df.columns:
        df['published_at'] = pd.to_datetime(df['published_at'])
        df['published_date'] = df['published_at'].dt.date
    
    return df

def create_sentiment_pie_chart(df):
    """Create sentiment distribution pie chart"""
    sentiment_counts = df['sentiment'].value_counts()
    
    colors = {
        'Positive': '#2ecc71',
        'Neutral': '#95a5a6',
        'Negative': '#e74c3c'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        marker=dict(colors=[colors.get(s, '#3498db') for s in sentiment_counts.index]),
        hole=0.4,
        textposition='inside',
        textinfo='percent+label'
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        height=400,
        showlegend=True
    )
    
    return fig

def create_source_bar_chart(df, top_n=10):
    """Create top sources bar chart"""
    source_counts = df['source'].value_counts().head(top_n)
    
    fig = go.Figure(data=[go.Bar(
        x=source_counts.values,
        y=source_counts.index,
        orientation='h',
        marker=dict(color='#3498db'),
        text=source_counts.values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title=f"Top {top_n} News Sources",
        xaxis_title="Number of Articles",
        yaxis_title="Source",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_timeline_chart(df):
    """Create sentiment timeline chart"""
    timeline = df.groupby(['published_date', 'sentiment']).size().reset_index(name='count')
    
    colors = {
        'Positive': '#2ecc71',
        'Neutral': '#95a5a6',
        'Negative': '#e74c3c'
    }
    
    fig = go.Figure()
    
    for sentiment in timeline['sentiment'].unique():
        sentiment_data = timeline[timeline['sentiment'] == sentiment]
        fig.add_trace(go.Scatter(
            x=sentiment_data['published_date'],
            y=sentiment_data['count'],
            mode='lines+markers',
            name=sentiment,
            line=dict(color=colors.get(sentiment, '#3498db'), width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Sentiment Timeline",
        xaxis_title="Date",
        yaxis_title="Number of Articles",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_score_histogram(df):
    """Create sentiment score distribution histogram"""
    fig = go.Figure(data=[go.Histogram(
        x=df['sentiment_score'],
        nbinsx=30,
        marker=dict(
            color=df['sentiment_score'],
            colorscale='RdYlGn',
            line=dict(color='black', width=1)
        )
    )])
    
    # Add threshold lines
    fig.add_vline(
        x=config.SENTIMENT_POSITIVE_THRESHOLD,
        line_dash="dash",
        line_color="green",
        annotation_text="Positive",
        annotation_position="top"
    )
    
    fig.add_vline(
        x=config.SENTIMENT_NEGATIVE_THRESHOLD,
        line_dash="dash",
        line_color="red",
        annotation_text="Negative",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Sentiment Score Distribution",
        xaxis_title="Sentiment Score",
        yaxis_title="Frequency",
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<div class="main-header">📰 News Sentiment Analysis Dashboard</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
    
    if df.empty:
        st.warning("⚠️ No data available. Please run the main application to collect and analyze news articles.")
        st.info("💡 Run `python main.py` to fetch and analyze news articles.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Sentiment filter
    sentiments = ['All'] + list(df['sentiment'].unique())
    selected_sentiment = st.sidebar.selectbox("Sentiment", sentiments)
    
    # Source filter
    sources = ['All'] + sorted(df['source'].unique())
    selected_source = st.sidebar.selectbox("Source", sources)
    
    # Date range filter
    if 'published_date' in df.columns:
        min_date = df['published_date'].min()
        max_date = df['published_date'].max()
        
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_sentiment != 'All':
        filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]
    
    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['source'] == selected_source]
    
    if 'published_date' in filtered_df.columns and len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['published_date'] >= date_range[0]) &
            (filtered_df['published_date'] <= date_range[1])
        ]
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.info(f"🔄 Auto-refresh: Every {config.DASHBOARD_REFRESH_INTERVAL // 60} minutes")
    st.sidebar.info(f"📊 Total Articles: {len(df)}")
    st.sidebar.info(f"🎯 Filtered Articles: {len(filtered_df)}")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(filtered_df)
        st.metric("Total Articles", total)
    
    with col2:
        positive = len(filtered_df[filtered_df['sentiment'] == 'Positive'])
        positive_pct = (positive / total * 100) if total > 0 else 0
        st.metric("Positive", f"{positive} ({positive_pct:.1f}%)")
    
    with col3:
        neutral = len(filtered_df[filtered_df['sentiment'] == 'Neutral'])
        neutral_pct = (neutral / total * 100) if total > 0 else 0
        st.metric("Neutral", f"{neutral} ({neutral_pct:.1f}%)")
    
    with col4:
        negative = len(filtered_df[filtered_df['sentiment'] == 'Negative'])
        negative_pct = (negative / total * 100) if total > 0 else 0
        st.metric("Negative", f"{negative} ({negative_pct:.1f}%)")
    
    # Charts
    st.markdown("---")
    
    # Row 1: Pie chart and bar chart
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_df.empty:
            st.plotly_chart(create_sentiment_pie_chart(filtered_df), use_container_width=True)
    
    with col2:
        if not filtered_df.empty:
            st.plotly_chart(create_source_bar_chart(filtered_df), use_container_width=True)
    
    # Row 2: Timeline and histogram
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_df.empty and 'published_date' in filtered_df.columns:
            st.plotly_chart(create_timeline_chart(filtered_df), use_container_width=True)
    
    with col2:
        if not filtered_df.empty and 'sentiment_score' in filtered_df.columns:
            st.plotly_chart(create_score_histogram(filtered_df), use_container_width=True)
    
    # Recent articles table
    st.markdown("---")
    st.subheader("📄 Recent Articles")
    
    if not filtered_df.empty:
        # Select columns to display
        display_cols = ['title', 'source', 'sentiment', 'sentiment_score', 'published_at']
        display_cols = [col for col in display_cols if col in filtered_df.columns]
        
        # Sort by date
        if 'published_at' in filtered_df.columns:
            display_df = filtered_df.sort_values('published_at', ascending=False)
        else:
            display_df = filtered_df
        
        # Display table
        st.dataframe(
            display_df[display_cols].head(20),
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Data (CSV)",
            data=csv,
            file_name=f"news_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No articles match the selected filters.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: gray;'>"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Built with Apache Spark + MongoDB + Streamlit"
        f"</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
