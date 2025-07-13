"""
Signals triggered on article save events.

On approval, sends emails to subscribers and posts to X (Twitter) via OAuth.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from requests_oauthlib import OAuth1Session
from .models import Article


@receiver(post_save, sender=Article)
def notify_on_approval(sender, instance, created, **kwargs):
    """
    Notify readers and post to X when an article is approved.

    - Emails are sent to all subscribed readers of the publisher and journalist.
    - A post is published to X using OAuth credentials.
    - Triggered only on update (not creation) where approved and not flagged for revision.
    """
    if not created and instance.approved and not instance.needs_revision:
        subject = f"New Article: {instance.title}"
        message = (
            f"{instance.description}\n\n"
            f"Read more at: http://127.0.0.1:8000/articles/{instance.id}/"
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        publisher_subs = instance.publisher.subscribed_readers.all()
        journalist_subs = instance.author.reader_subscribers.all()
        recipients = set([
            u.email for u in publisher_subs.union(journalist_subs) if u.email
        ])

        if recipients:
            send_mail(subject, message, from_email, list(recipients), fail_silently=True)

        try:
            twitter = OAuth1Session(
                settings.X_API_KEY,
                settings.X_API_SECRET,
                settings.X_ACCESS_TOKEN,
                settings.X_ACCESS_TOKEN_SECRET
            )
            tweet = {
                "text": f"{instance.title} by {instance.author.username}\n"
                        f"Read: http://127.0.0.1:8000/articles/{instance.id}/"
            }
            response = twitter.post("https://api.twitter.com/2/tweets", json=tweet)
            response.raise_for_status()
        except Exception as e:
            print("Error posting to X:", e)
