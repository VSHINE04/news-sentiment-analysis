from sentiment_analyzer import SentimentAnalyzer

articles = [{
	'title': 'Test',
	'description': 'Test article',
	'full_text': 'Amazing breakthrough in AI technology. Markets plunge amid concerns.',
	'source': 'Test',
	'author': 'Tester'
}]

analyzer = SentimentAnalyzer()
df = analyzer.analyze_articles(articles)
print('DF is None?', df is None)
if df is not None:
	print('Row count:', df.count())
	df.select('title','sentiment','sentiment_score').show(truncate=False)

analyzer.stop()
