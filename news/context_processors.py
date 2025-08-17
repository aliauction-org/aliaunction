from .models import Article

def latest_news(request):
    """Context processor to include latest news articles in all templates"""
    try:
        latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
        return {
            'latest_news_articles': latest_articles
        }
    except:
        return {
            'latest_news_articles': []
        } 