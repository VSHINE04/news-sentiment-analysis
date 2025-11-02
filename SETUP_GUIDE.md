# Quick Setup Guide

Get started with News Sentiment Analysis in 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Get API Keys (2 minutes)

#### NewsAPI Key
1. Visit: https://newsapi.org/register
2. Sign up (free)
3. Copy your API key

#### MongoDB Atlas (Optional - can use existing)
1. Visit: https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string

### Step 2: Configure (1 minute)

Edit `.env` file:
```env
NEWS_API_KEY=your_newsapi_key_here
MONGODB_URI=your_mongodb_connection_string_here
```

### Step 3: Install (2 minutes)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Test

```powershell
python test_setup.py
```

### Step 5: Run!

```powershell
run.bat
```

## 🎯 Quick Commands

### Run Main Application
```powershell
run.bat          # Windows CMD
.\run.ps1        # PowerShell
python main.py   # Direct
```

### Run Dashboard
```powershell
run_dashboard.bat
# Opens at http://localhost:8501
```

### Quick Test
```powershell
python run_quick_test.py
```

## 📋 Menu Options

1. **Search by keyword** - Find news about any topic
2. **Top headlines** - Latest news by category
3. **Analyze stored** - Work with saved articles
4. **Statistics** - View database stats
5. **Clear database** - Delete all articles
6. **Exit** - Close application

## 🎨 Dashboard Features

Access: `http://localhost:8501`

**Filters:**
- Sentiment (Positive/Neutral/Negative)
- Source
- Date Range

**Charts:**
- Sentiment pie chart
- Source bar chart
- Timeline trends
- Score histogram

## ⚙️ Configuration

Edit `config.py` to customize:
- Sentiment thresholds
- Spark settings
- Chart styles
- Output directory

## 🔧 Troubleshooting

### Issue: Module not found
```powershell
pip install -r requirements.txt
```

### Issue: MongoDB connection failed
- Check `MONGODB_URI` in `.env`
- Verify internet connection
- Check MongoDB Atlas IP whitelist

### Issue: NewsAPI rate limit
- Free tier: 100 requests/day
- Wait 24 hours or upgrade plan

### Issue: Spark errors on Windows
- Use Python 3.11 (not 3.12)
- Already optimized in code

## 📊 Quick Example

```powershell
python main.py
# Select: 1 (Search by keyword)
# Enter: artificial intelligence
# Days: 7
# Articles: 50
# Save: y
# Visualize: y
```

Results saved to:
- MongoDB database
- `output/` folder (charts)

## 🚀 Next Steps

1. ✅ Run your first analysis
2. ✅ Check the dashboard
3. ✅ Try different keywords
4. ✅ Explore visualizations
5. ✅ Customize settings

## 📞 Need Help?

Run diagnostics:
```powershell
python test_setup.py
python run_quick_test.py
```

Check:
- Python version (3.8+)
- Virtual environment active
- All packages installed
- API keys configured

## 🎉 You're Ready!

The system is now ready to:
- ✅ Fetch news from 80,000+ sources
- ✅ Analyze sentiment with Spark
- ✅ Store in MongoDB
- ✅ Create visualizations
- ✅ Display interactive dashboard

**Start analyzing news sentiment now!** 🚀

---

For detailed documentation, see `README.md`
