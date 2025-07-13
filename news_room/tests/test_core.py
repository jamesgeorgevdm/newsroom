from django.test import TestCase
from django.urls import reverse
from news_room.models import CustomUser, Publisher, Article


class CoreModelsTests(TestCase):
    """
    Tests for core model behavior like subscriptions and article creation.
    """
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.journalist = CustomUser.objects.create_user(username="journalist1", password="testpass", role="journalist")
        self.reader = CustomUser.objects.create_user(username="reader1", password="testpass", role="reader")

        self.article = Article.objects.create(
            title="Test Article",
            description="Desc",
            content="Full content here",
            approved=True,
            author=self.journalist,
            publisher=self.publisher
        )

        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertTrue(self.article.approved)

    def test_reader_subscriptions(self):
        self.assertIn(self.publisher, self.reader.subscribed_publishers.all())
        self.assertIn(self.journalist, self.reader.subscribed_journalists.all())


class CoreViewsTests(TestCase):
    """
    Tests for basic view access and dashboard rendering.
    """
    def setUp(self):
        self.journalist = CustomUser.objects.create_user(username="journalist1", password="testpass", role="journalist")

    def test_dashboard_access(self):
        login_successful = self.client.login(username="journalist1", password="testpass")
        self.assertTrue(login_successful)

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "journalist1")
