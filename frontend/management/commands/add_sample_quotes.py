from django.core.management.base import BaseCommand
from frontend.models import Quote


class Command(BaseCommand):
    help = 'Add sample quotes with categories'

    def handle(self, *args, **options):
        sample_quotes = [
            {
                'quote_text': 'For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, to give you hope and a future.',
                'author': 'God',
                'source': 'Jeremiah 29:11',
                'category': 'hope',
                'is_featured': True,
                'order': 1
            },
            {
                'quote_text': 'And whoever gives one of these little ones even a cup of cold water because he is a disciple, truly, I say to you, he will by no means lose his reward.',
                'author': 'Jesus Christ',
                'source': 'Matthew 10:42',
                'category': 'service',
                'is_featured': True,
                'order': 2
            },
            {
                'quote_text': 'Religion that is pure and undefiled before God the Father is this: to visit orphans and widows in their affliction, and to keep oneself unstained from the world.',
                'author': 'James',
                'source': 'James 1:27',
                'category': 'service',
                'is_featured': True,
                'order': 3
            },
            {
                'quote_text': 'Let your light shine before others, that they may see your good deeds and glorify your Father in heaven.',
                'author': 'Jesus Christ',
                'source': 'Matthew 5:16',
                'category': 'witness',
                'is_featured': True,
                'order': 4
            },
            {
                'quote_text': 'Now faith is confidence in what we hope for and assurance about what we do not see.',
                'author': 'Paul',
                'source': 'Hebrews 11:1',
                'category': 'faith',
                'is_featured': False,
                'order': 5
            },
            {
                'quote_text': 'Above all, love each other deeply, because love covers over a multitude of sins.',
                'author': 'Peter',
                'source': '1 Peter 4:8',
                'category': 'love',
                'is_featured': False,
                'order': 6
            },
            {
                'quote_text': 'Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.',
                'author': 'Jesus Christ',
                'source': 'John 14:27',
                'category': 'peace',
                'is_featured': False,
                'order': 7
            },
            {
                'quote_text': 'The joy of the Lord is your strength.',
                'author': 'Nehemiah',
                'source': 'Nehemiah 8:10',
                'category': 'joy',
                'is_featured': False,
                'order': 8
            },
            {
                'quote_text': 'Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.',
                'author': 'Solomon',
                'source': 'Proverbs 3:5-6',
                'category': 'wisdom',
                'is_featured': False,
                'order': 9
            },
            {
                'quote_text': 'Truly I tell you, whatever you did for one of the least of these brothers and sisters of mine, you did for me.',
                'author': 'Jesus Christ',
                'source': 'Matthew 25:40',
                'category': 'service',
                'is_featured': False,
                'order': 10
            }
        ]

        # Clear existing quotes
        Quote.objects.all().delete()
        
        # Add sample quotes
        for quote_data in sample_quotes:
            Quote.objects.create(**quote_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {len(sample_quotes)} sample quotes!')
        )
