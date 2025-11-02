"""
Visualizer Module
Creates various charts and visualizations for sentiment analysis results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import os
import config

class Visualizer:
    """Creates visualizations for news sentiment analysis"""
    
    def __init__(self):
        """Initialize visualizer with style settings"""
        # Set style
        try:
            plt.style.use(config.CHART_STYLE)
        except:
            plt.style.use('seaborn-v0_8')
        
        # Set color palette
        sns.set_palette("husl")
        
        # Create output directory
        config.create_output_directory()
        
        print("✅ Visualizer initialized")
    
    def plot_sentiment_distribution(self, df, save=True):
        """
        Create pie chart showing sentiment distribution
        
        Args:
            df (DataFrame): DataFrame with sentiment column
            save (bool): Whether to save the plot
        
        Returns:
            str: Path to saved file or None
        """
        try:
            # Convert to Pandas if needed
            if hasattr(df, 'toPandas'):
                pdf = df.toPandas()
            else:
                pdf = df
            
            # Count sentiments
            sentiment_counts = pdf['sentiment'].value_counts()
            
            # Create figure
            fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
            
            # Define colors
            colors = {
                'Positive': '#2ecc71',  # Green
                'Neutral': '#95a5a6',   # Gray
                'Negative': '#e74c3c'   # Red
            }
            
            plot_colors = [colors.get(s, '#3498db') for s in sentiment_counts.index]
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                sentiment_counts.values,
                labels=sentiment_counts.index,
                autopct='%1.1f%%',
                colors=plot_colors,
                startangle=90,
                textprops={'fontsize': 12, 'weight': 'bold'}
            )
            
            # Enhance text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(14)
            
            ax.set_title('Sentiment Distribution', fontsize=16, weight='bold', pad=20)
            
            plt.tight_layout()
            
            # Save or show
            if save:
                filepath = os.path.join(config.OUTPUT_DIR, f'sentiment_distribution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                print(f"✅ Saved: {filepath}")
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        
        except Exception as e:
            print(f"❌ Error creating sentiment distribution plot: {str(e)}")
            return None
    
    def plot_source_distribution(self, df, top_n=10, save=True):
        """
        Create bar chart showing top news sources
        
        Args:
            df (DataFrame): DataFrame with source column
            top_n (int): Number of top sources to show
            save (bool): Whether to save the plot
        
        Returns:
            str: Path to saved file or None
        """
        try:
            # Convert to Pandas if needed
            if hasattr(df, 'toPandas'):
                pdf = df.toPandas()
            else:
                pdf = df
            
            # Count sources
            source_counts = pdf['source'].value_counts().head(top_n)
            
            # Create figure
            fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
            
            # Create horizontal bar chart
            bars = ax.barh(range(len(source_counts)), source_counts.values, color='#3498db')
            
            # Customize
            ax.set_yticks(range(len(source_counts)))
            ax.set_yticklabels(source_counts.index)
            ax.set_xlabel('Number of Articles', fontsize=12, weight='bold')
            ax.set_title(f'Top {top_n} News Sources', fontsize=16, weight='bold', pad=20)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, source_counts.values)):
                ax.text(value, i, f' {value}', va='center', fontsize=10, weight='bold')
            
            ax.invert_yaxis()  # Highest on top
            plt.tight_layout()
            
            # Save or show
            if save:
                filepath = os.path.join(config.OUTPUT_DIR, f'source_distribution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                print(f"✅ Saved: {filepath}")
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        
        except Exception as e:
            print(f"❌ Error creating source distribution plot: {str(e)}")
            return None
    
    def plot_sentiment_timeline(self, df, save=True):
        """
        Create line chart showing sentiment trends over time
        
        Args:
            df (DataFrame): DataFrame with published_at and sentiment columns
            save (bool): Whether to save the plot
        
        Returns:
            str: Path to saved file or None
        """
        try:
            # Convert to Pandas if needed
            if hasattr(df, 'toPandas'):
                pdf = df.toPandas()
            else:
                pdf = df
            
            # Convert published_at to datetime
            pdf['published_date'] = pd.to_datetime(pdf['published_at']).dt.date
            
            # Group by date and sentiment
            timeline = pdf.groupby(['published_date', 'sentiment']).size().reset_index(name='count')
            
            # Pivot for plotting
            timeline_pivot = timeline.pivot(index='published_date', columns='sentiment', values='count').fillna(0)
            
            # Create figure
            fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
            
            # Define colors
            colors = {
                'Positive': '#2ecc71',
                'Neutral': '#95a5a6',
                'Negative': '#e74c3c'
            }
            
            # Plot lines
            for sentiment in timeline_pivot.columns:
                ax.plot(
                    timeline_pivot.index,
                    timeline_pivot[sentiment],
                    marker='o',
                    linewidth=2,
                    label=sentiment,
                    color=colors.get(sentiment, '#3498db')
                )
            
            # Customize
            ax.set_xlabel('Date', fontsize=12, weight='bold')
            ax.set_ylabel('Number of Articles', fontsize=12, weight='bold')
            ax.set_title('Sentiment Timeline', fontsize=16, weight='bold', pad=20)
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Save or show
            if save:
                filepath = os.path.join(config.OUTPUT_DIR, f'sentiment_timeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                print(f"✅ Saved: {filepath}")
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        
        except Exception as e:
            print(f"❌ Error creating sentiment timeline plot: {str(e)}")
            return None
    
    def plot_score_distribution(self, df, save=True):
        """
        Create histogram showing distribution of sentiment scores
        
        Args:
            df (DataFrame): DataFrame with sentiment_score column
            save (bool): Whether to save the plot
        
        Returns:
            str: Path to saved file or None
        """
        try:
            # Convert to Pandas if needed
            if hasattr(df, 'toPandas'):
                pdf = df.toPandas()
            else:
                pdf = df
            
            # Create figure
            fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
            
            # Create histogram with color gradient
            n, bins, patches = ax.hist(
                pdf['sentiment_score'],
                bins=30,
                edgecolor='black',
                alpha=0.7
            )
            
            # Color gradient from red (negative) to green (positive)
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            
            # Normalize colors
            col_norm = (bin_centers - bin_centers.min()) / (bin_centers.max() - bin_centers.min())
            
            for c, p in zip(col_norm, patches):
                # Red to yellow to green gradient
                if c < 0.5:
                    color = plt.cm.RdYlGn(c)
                else:
                    color = plt.cm.RdYlGn(c)
                p.set_facecolor(color)
            
            # Add threshold lines
            ax.axvline(config.SENTIMENT_POSITIVE_THRESHOLD, color='green', linestyle='--', linewidth=2, label='Positive Threshold')
            ax.axvline(config.SENTIMENT_NEGATIVE_THRESHOLD, color='red', linestyle='--', linewidth=2, label='Negative Threshold')
            
            # Customize
            ax.set_xlabel('Sentiment Score', fontsize=12, weight='bold')
            ax.set_ylabel('Frequency', fontsize=12, weight='bold')
            ax.set_title('Sentiment Score Distribution', fontsize=16, weight='bold', pad=20)
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            
            # Save or show
            if save:
                filepath = os.path.join(config.OUTPUT_DIR, f'score_distribution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                print(f"✅ Saved: {filepath}")
                plt.close()
                return filepath
            else:
                plt.show()
                return None
        
        except Exception as e:
            print(f"❌ Error creating score distribution plot: {str(e)}")
            return None
    
    def create_all_plots(self, df):
        """
        Create all visualization plots
        
        Args:
            df (DataFrame): DataFrame with analysis results
        
        Returns:
            dict: Dictionary of saved file paths
        """
        print("\n📊 Creating visualizations...")
        
        files = {
            'sentiment_distribution': self.plot_sentiment_distribution(df),
            'source_distribution': self.plot_source_distribution(df),
            'sentiment_timeline': self.plot_sentiment_timeline(df),
            'score_distribution': self.plot_score_distribution(df)
        }
        
        print(f"\n✅ Created {len([f for f in files.values() if f])} visualizations")
        return files

# Example usage
if __name__ == "__main__":
    # Test with sample data
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Create sample data
    dates = [datetime.now() - timedelta(days=i) for i in range(7)]
    sample_data = pd.DataFrame({
        'sentiment': ['Positive', 'Negative', 'Neutral', 'Positive', 'Positive', 'Neutral', 'Negative'] * 10,
        'sentiment_score': [0.5, -0.3, 0.0, 0.6, 0.4, 0.01, -0.5] * 10,
        'source': ['BBC', 'CNN', 'Reuters', 'BBC', 'TechCrunch', 'CNN', 'Reuters'] * 10,
        'published_at': [dates[i % 7] for i in range(70)]
    })
    
    # Create visualizer
    viz = Visualizer()
    
    # Create all plots
    files = viz.create_all_plots(sample_data)
    
    print(f"\n📁 Saved files:")
    for name, filepath in files.items():
        if filepath:
            print(f"  - {name}: {filepath}")
