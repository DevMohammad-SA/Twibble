from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from tweets.models import Tweet
from users.models import TwibbleUser

from .models import Notification

# like singals


@receiver(m2m_changed, sender=Tweet.likes.through)
def notify_on_like(sender, instance, action, pk_set, **kwargs):
    # 'instance' is the tweet being liked
    # 'pk_set' is the list of User_IDs who liked it
    if action == "post_add":  # only notify when like is ADDED (not REMOVED)
        for user_id in pk_set:
            user = TwibbleUser.objects.get(pk=user_id)

            # don't notify if user liked his own tweet
            if user != instance.user:
                Notification.objects.create(
                    sender=user,
                    recipient=instance.user,
                    notification_type="like",
                    tweet=instance,
                )


@receiver(m2m_changed, sender=TwibbleUser.following.through)
def notify_on_follow(sender, instance, action, pk_set, **kwargs):
    # instance here is the user doing the following (the follower)
    # 'pk_set' is the User ID being followed (the target)
    if action == "post_add":
        for target_id in pk_set:
            target_user = TwibbleUser.objects.get(pk=target_id)

            Notification.objects.create(
                sender=instance, recipient=target_user, notification_type="follow"
            )


@receiver(post_save, sender=Tweet)
def notify_on_reply(sender, instance, created, **kwargs):
    if created and instance.is_reply and instance.user != instance.parent_tweet.user:
        Notification.objects.create(
            sender=instance.user,
            recipient=instance.parent_tweet.user,
            notification_type="reply",
            tweet=instance,
        )
