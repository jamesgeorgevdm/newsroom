from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from news_room.models import CustomUser, Publisher, Article


class ArticleAPITests(APITestCase):
    """
    Tests for article-related API endpoints, including publisher and journalist filters.
    """
    def setUp(self):
        self.client = APIClient()

        # Create test publishers
        self.publisher1 = Publisher.objects.create(name="Publisher 1")
        self.publisher2 = Publisher.objects.create(name="Publisher 2")

        # Create test journalists
        self.journalist1 = CustomUser.objects.create_user(username="j1", password="pass", role="journalist")
        self.journalist2 = CustomUser.objects.create_user(username="j2", password="pass", role="journalist")

        # Create a reader and set subscriptions
        self.reader = CustomUser.objects.create_user(username="reader", password="pass", role="reader")
        self.reader.subscribed_publishers.add(self.publisher1)
        self.reader.subscribed_journalists.add(self.journalist2)

        # Create approved and unapproved articles
        self.article_pub1 = Article.objects.create(
            title="Pub1 Article",
            description="Desc",
            content="Content",
            approved=True,
            author=self.journalist1,
            publisher=self.publisher1
        )
        self.article_pub2 = Article.objects.create(
            title="Pub2 Article",
            description="Desc",
            content="Content",
            approved=True,
            author=self.journalist2,
            publisher=self.publisher2
        )
        self.article_unapproved = Article.objects.create(
            title="Unapproved",
            description="Desc",
            content="Content",
            approved=False,
            author=self.journalist2,
            publisher=self.publisher2
        )

    def test_api_requires_authentication(self):
        url = reverse('publisher_articles_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_articles_for_subscribed_publishers(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('publisher_articles_api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a.get('title') for a in response.data]
        self.assertIn("Pub1 Article", titles)
        self.assertNotIn("Pub2 Article", titles)

    def test_get_articles_for_subscribed_journalists(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('journalist_articles_api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a.get('title') for a in response.data]
        self.assertIn("Pub2 Article", titles)
        self.assertNotIn("Pub1 Article", titles)

    def test_unapproved_articles_are_not_returned(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('journalist_articles_api')
        response = self.client.get(url)
        titles = [a.get('title') for a in response.data]
        self.assertNotIn("Unapproved", titles)
