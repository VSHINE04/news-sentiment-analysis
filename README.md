# News Sentiment Analysis with Apache Spark

A complete real-time ETL pipeline for news sentiment analysis using Apache Spark, MongoDB, and NewsAPI. This project collects news articles, performs sentiment analysis using VADER and TextBlob, stores results in MongoDB, and visualizes insights through interactive dashboards.

![Project Status](https://img.shields.io/badge/status-production-green)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Features

### Core Capabilities
- ✅ **Real-time News Collection** - Fetch articles from 80,000+ sources via NewsAPI
- ✅ **Distributed Processing** - Apache Spark for scalable sentiment analysis
- ✅ **Dual Sentiment Engine** - VADER + TextBlob for accurate sentiment scoring
- ✅ **Cloud Storage** - MongoDB Atlas for persistent data storage
- ✅ **Rich Visualizations** - 4 chart types with Matplotlib/Seaborn
- ✅ **Interactive Dashboard** - Real-time Streamlit UI with filters
- ✅ **Windows Optimized** - Fully compatible with Windows + PySpark

### Analysis Capabilities
- Keyword-based news search
- Category-based headlines (7 categories)
- Multi-source aggregation
- Time-series sentiment tracking
- Source-level analytics
- Score distribution analysis

## 📊 Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  NewsAPI    │────▶│   Apache     │────▶│   MongoDB   │────▶│ Streamlit    │
│  (80K+ src) │     │   Spark      │     │   Atlas     │     │  Dashboard   │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                           │
                           ├─ VADER Sentiment
                           ├─ TextBlob Analysis
                           └─ Data Cleaning
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.11 recommended for Windows)
- NewsAPI Key (free at https://newsapi.org/register)
- MongoDB Atlas URI (free at https://www.mongodb.com/cloud/atlas)

### Installation

1. **Clone or download this project**
```bash
cd news-sentiment-analysis
```

2. **Create virtual environment**
```powershell
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure API keys**
- Copy `.env` file and add your keys:
```env
NEWS_API_KEY=your_newsapi_key_here
MONGODB_URI=your_mongodb_uri_here
```

5. **Run setup test**
```powershell
python test_setup.py
```

### Running the Application

**Option 1: Using run scripts (Recommended)**
```powershell
# Windows CMD
run.bat

# PowerShell
.\run.ps1
```

**Option 2: Manual execution**
```powershell
python main.py
```

**Option 3: Dashboard only**
```powershell
run_dashboard.bat
# or
streamlit run dashboard.py
```

## 📁 Project Structure

```
news-sentiment-analysis/
├── Core Application
│   ├── main.py                 # Main orchestration
│   ├── config.py               # Configuration management
│   ├── news_collector.py       # NewsAPI integration
│   ├── sentiment_analyzer.py   # Spark sentiment analysis
│   ├── mongodb_handler.py      # Database operations
│   └── visualizer.py           # Chart generation
│
├── Dashboard
│   └── dashboard.py            # Streamlit interactive UI
│
├── Run Scripts
│   ├── run.bat                 # Windows CMD launcher
│   ├── run.ps1                 # PowerShell launcher
│   ├── run_dashboard.bat       # Dashboard launcher
│   ├── test_setup.py           # Setup verification
│   └── run_quick_test.py       # Quick system test
│
├── Configuration
│   ├── .env                    # API credentials
│   └── requirements.txt        # Python dependencies
│
└── Documentation
    ├── README.md               # This file
    └── SETUP_GUIDE.md          # Quick setup guide
```

## 🎮 Usage Guide

### Main Menu Options

1. **Search news by keyword**
   - Enter any search term (e.g., "climate change", "AI")
   - Specify date range (1-7 days)
   - Set max articles (1-100)
   - Auto-analyzes sentiment
   - Saves to MongoDB
   - Generates visualizations

2. **Fetch top headlines by category**
   - Choose from 7 categories (business, tech, sports, etc.)
   - Fetches latest headlines
   - Performs sentiment analysis
   - Creates reports

3. **Analyze stored articles**
   - Retrieves articles from MongoDB
   - Re-analyzes if needed
   - Generates fresh visualizations

4. **View statistics**
   - Total articles count
   - Sentiment distribution
   - Top sources
   - Average scores
   - Date ranges

5. **Clear database**
   - Delete all stored articles
   - Requires confirmation

#+ News Sentiment Analysis

Lightweight ETL and analysis pipeline that collects news articles, runs simple sentiment analysis (VADER + TextBlob), stores results in MongoDB, and provides a Streamlit dashboard for inspection and visualization.

This repository contains scripts and helpers to fetch news from NewsAPI, process them with PySpark (or locally for small datasets), persist results to MongoDB, and visualize insights.

Note: No license file is included with this repository per project owner's request.

## Quick start

Prerequisites
- Python 3.8+
- A NewsAPI key (https://newsapi.org)
- A MongoDB URI (Atlas or local)

Installation
1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env` (if present) and fill in your keys:

```
NEWS_API_KEY=your_key_here
MONGODB_URI=your_mongo_uri_here
```

Run a quick setup test:

```powershell
python test_setup.py
```

Run the project
- To run the full pipeline: `python main.py`
- To run the dashboard: `streamlit run dashboard.py` or use `run_dashboard.bat`

## Project layout

- `main.py` — orchestration of fetch → analyze → store
- `news_collector.py` — NewsAPI integration
- `sentiment_analyzer.py` — sentiment scoring (VADER + TextBlob)
- `mongodb_handler.py` — helpers to read/write to MongoDB
- `dashboard.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies

## Notes

- The project includes Windows-specific PySpark environment tweaks to avoid common errors on Windows.
- The `.env` file is excluded from source control to keep API keys private.
- No license is included. If you want to add a license, specify which one and I can add it.

## Contributing

This project is maintained by the repository owner. If you'd like to contribute, fork the repo and open a pull request, or contact the owner for collaboration.

## Uploading to GitHub

If you want me to push these changes to `https://github.com/VSHINE04/news-sentiment-analysis`, I can initialize a git repo, commit the updated README and (optionally) other files, and attempt to push — but pushing requires write access or credentials on your machine. If the push fails due to authentication, I'll provide exact commands and next steps.

---

Short and actionable README prepared.
