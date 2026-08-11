from django.test import TestCase, override_settings
from django.core import mail
from unittest.mock import patch
from news_room.models import Article, CustomUser, Publisher


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class SignalsTests(TestCase):
    """
    Tests that signals correctly trigger emails and X posts upon article approval.
    """
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Pub")
        self.journalist = CustomUser.objects.create_user(
            username="j1", password="pass", role="journalist", email="j1@example.com"
        )
        self.reader = CustomUser.objects.create_user(
            username="reader", password="pass", role="reader", email="reader@example.com"
        )

        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

        self.article = Article.objects.create(
            title="Test Article",
            description="desc",
            content="content",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
            needs_revision=False
        )

    @patch('news_room.signals.OAuth1Session')
    def test_tweet_posted_on_approval(self, mock_oauth_session):
        mock_client = mock_oauth_session.return_value
        mock_response = mock_client.post.return_value
        mock_response.raise_for_status.return_value = None

        self.article.approved = True
        self.article.save()  # Triggers post_save signal

        mock_client.post.assert_called_once()

    def test_email_sent_on_approval(self):
        self.article.approved = True
        self.article.save()
        self.assertGreater(len(mail.outbox), 0)
        self.assertIn("Test Article", mail.outbox[0].subject)
