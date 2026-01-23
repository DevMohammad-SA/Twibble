from django.db.models import Count
from django.http import request
from .models import Tag
from .forms import TweetForm


def trending_tags(request):
    # Annotate each tag with a 'tweet_count' field
    # Order by that count (descending) and take the top 5
    tags = Tag.objects.annotate(tweet_count=Count("tweets")).order_by("-tweet_count")[
        :5
    ]
    return {"trending_tags": tags}


def post_tweet_form(request):
    form = TweetForm(request.POST)
    
    return {"post_tweet_form":form}
