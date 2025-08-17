from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from news.models import Category, Tag, Article, Comment
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the news system with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample news data...')

        # Create categories
        categories_data = [
            {'name': 'Auction Tips', 'description': 'Essential tips and strategies for successful bidding'},
            {'name': 'Success Stories', 'description': 'Inspiring stories from successful bidders and sellers'},
            {'name': 'Market Trends', 'description': 'Latest trends and insights in the auction market'},
            {'name': 'How-to Guides', 'description': 'Step-by-step guides for auction participation'},
            {'name': 'Industry News', 'description': 'Latest news and updates from the auction industry'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_data = [
            'bidding', 'strategy', 'antiques', 'art', 'jewelry', 'electronics',
            'collectibles', 'tips', 'success', 'market', 'trends', 'guide',
            'beginner', 'expert', 'investment', 'valuation', 'restoration'
        ]

        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Get or create a user for articles
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created admin user')

        # Create sample articles
        articles_data = [
            {
                'title': 'How to Win Your First Auction: A Complete Beginner\'s Guide',
                'category': categories['How-to Guides'],
                'tags': [tags['beginner'], tags['tips'], tags['strategy']],
                'content': '<h2>Getting Started with Auctions</h2><p>AuctionVistas is your gateway to exciting bidding opportunities. Whether you\'re a first-time bidder or looking to expand your collection, this guide will help you navigate the auction process with confidence.</p><h3>1. Research is Key</h3><p>Before placing your first bid, take time to research the items you\'re interested in. Look at similar items that have sold recently to understand market values.</p>',
                'excerpt': 'Learn the essential strategies and tips to successfully participate in your first auction. From research to bidding, this comprehensive guide covers everything beginners need to know.',
                'is_featured': True,
                'published_at': timezone.now() - timedelta(days=2)
            },
            {
                'title': 'Spotlight: Rare Finds of the Month - December 2024',
                'category': categories['Market Trends'],
                'tags': [tags['antiques'], tags['collectibles'], tags['market'], tags['trends']],
                'content': '<h2>December\'s Most Remarkable Discoveries</h2><p>This month has brought some truly extraordinary items to AuctionVistas, showcasing the incredible variety and value that can be found in our auctions.</p><h3>Ancient Roman Coin Collection</h3><p>A stunning collection of 15 Roman coins dating from 27 BC to 476 AD was discovered in a family estate.</p>',
                'excerpt': 'Discover the most remarkable items that came to auction this month, from ancient Roman coins to rare literary treasures.',
                'is_featured': True,
                'published_at': timezone.now() - timedelta(days=5)
            },
            {
                'title': 'The Psychology of Bidding: Understanding Auction Dynamics',
                'category': categories['Auction Tips'],
                'tags': [tags['strategy'], tags['expert'], tags['tips']],
                'content': '<h2>Understanding Auction Psychology</h2><p>Successful bidding isn\'t just about having the highest budget—it\'s about understanding the psychological dynamics at play in auction environments.</p><h3>The Competitive Drive</h3><p>Auctions naturally create competition, which can trigger emotional responses.</p>',
                'excerpt': 'Learn about the psychological factors that influence bidding behavior and how to use this knowledge to your advantage in auctions.',
                'is_featured': False,
                'published_at': timezone.now() - timedelta(days=8)
            },
            {
                'title': 'From Garage Sale to Gallery: Success Story of a $50,000 Discovery',
                'category': categories['Success Stories'],
                'tags': [tags['success'], tags['antiques'], tags['valuation'], tags['collectibles']],
                'content': '<h2>An Unlikely Discovery</h2><p>Sarah Johnson\'s story proves that incredible treasures can be found in the most unexpected places. What started as a routine garage sale purchase turned into a life-changing discovery.</p>',
                'excerpt': 'Read the incredible story of how a $25 garage sale purchase turned into a $52,000 auction sale.',
                'is_featured': False,
                'published_at': timezone.now() - timedelta(days=12)
            },
            {
                'title': 'Digital Art Auctions: The Future of Collecting',
                'category': categories['Industry News'],
                'tags': [tags['art'], tags['trends'], tags['market'], tags['investment']],
                'content': '<h2>The Rise of Digital Art</h2><p>Digital art has emerged as one of the fastest-growing segments in the auction market, with NFTs (Non-Fungible Tokens) leading the charge. AuctionVistas is at the forefront of this digital revolution.</p>',
                'excerpt': 'Explore the growing world of digital art auctions and NFTs. Learn how this new market is changing the way we collect and invest in art.',
                'is_featured': False,
                'published_at': timezone.now() - timedelta(days=15)
            }
        ]

        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'author': user,
                    'category': article_data['category'],
                    'content': article_data['content'],
                    'excerpt': article_data['excerpt'],
                    'status': 'published',
                    'is_featured': article_data['is_featured'],
                    'published_at': article_data['published_at']
                }
            )
            
            if created:
                # Add tags
                for tag in article_data['tags']:
                    article.tags.add(tag)
                
                self.stdout.write(f'Created article: {article.title}')
                
                # Add some sample comments
                comments_data = [
                    'Great article! Very helpful for beginners like me.',
                    'I learned a lot from this. Thanks for sharing!',
                    'Excellent tips. I\'ll definitely use these strategies.',
                ]
                
                for comment_text in comments_data:
                    comment = Comment.objects.create(
                        article=article,
                        author=user,
                        content=comment_text,
                        is_approved=True
                    )
                    self.stdout.write(f'  - Added comment: {comment_text[:50]}...')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample news data!')
        ) 