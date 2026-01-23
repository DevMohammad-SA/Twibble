import re
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def hashtag_links(text):
    # convert hastags into clickable links
    def replace_hashtag(match):
        tag_slug = match.group(1).lower()
        # Create the URL for this tag
        url = reverse("tweets:tag", args=[tag_slug])
        return f'<a href="{url}" class="text-primary text-decoration-none">#{match.group(1)}</a>'

    # Regex finds # followed by word characters
    # We use mark_safe so Django renders the HTML <a> tag instead of escaping it
    return mark_safe(re.sub(r"#(\w+)", replace_hashtag, text))
