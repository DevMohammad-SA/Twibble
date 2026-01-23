from django.db.models import Count
from .models import Tag


def trending_tags(request):
    # Annotate each tag with a 'tweet_count' field
    # Order by that count (descending) and take the top 5
    tags = Tag.objects.annotate(tweet_count=Count("tweets")).order_by("-tweet_count")[
        :5
    ]
    return {"trending_tags": tags}
