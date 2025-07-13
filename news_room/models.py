"""
User, publisher, article, and newsletter models for the NewsRoom app.

Includes custom user roles, relationship mappings, and core content models.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings


ROLE_CHOICES = (
    ('reader', 'Reader'),
    ('journalist', 'Journalist'),
    ('editor', 'Editor'),
)


class CustomUser(AbstractUser):
    """
    Custom user model with extended role support.

    Attributes:
        role (str): Role type ('reader', 'journalist', or 'editor').
        subscribed_publishers (QuerySet): Publishers this reader subscribes to.
        subscribed_journalists (QuerySet): Journalists this reader subscribes to.
        published_articles (QuerySet): Articles submitted by this journalist.
        published_newsletters (QuerySet): Newsletters published by this journalist.
    """

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscribed_publishers = models.ManyToManyField(
        'Publisher', blank=True, related_name='subscribed_readers'
    )
    subscribed_journalists = models.ManyToManyField(
        'CustomUser', blank=True, related_name='reader_subscribers'
    )

    published_articles = models.ManyToManyField(
        'Article', blank=True, related_name='journalist_articles'
    )
    published_newsletters = models.ManyToManyField(
        'Newsletter', blank=True, related_name='journalist_newsletters'
    )

    def save(self, *args, **kwargs):
        """
        Assigns user to group based on role and clears incompatible fields.

        This method ensures that role-specific associations remain exclusive.
        """
        super().save(*args, **kwargs)

        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role.capitalize())
            self.groups.clear()
            self.groups.add(group)

        if self.role == 'reader':
            self.published_articles.clear()
            self.published_newsletters.clear()

        elif self.role == 'journalist':
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()


class Publisher(models.Model):
    """
    A media organization that manages articles and newsletters.

    Attributes:
        name (str): Display name of the publisher.
        editors (QuerySet): Associated editor accounts.
        journalists (QuerySet): Associated journalist accounts.
    """

    name = models.CharField(max_length=255)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='editor_publishers', blank=True
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='journalist_publishers', blank=True
    )

    def __str__(self):
        """
        Returns:
            str: Name of the publisher.
        """
        return self.name


class Article(models.Model):
    """
    An article authored by a journalist and reviewed by editors.

    Attributes:
        title (str): Article headline.
        description (str): Brief summary or teaser.
        content (str): Full body of the article.
        approved (bool): Whether the article is approved for publishing.
        needs_revision (bool): Whether the article is flagged for edits.
        editor_feedback (str): Optional feedback from the editor.
        author (CustomUser): Journalist who wrote the article.
        publisher (Publisher): Publishing organization.
        created_at (datetime): Timestamp of initial creation.
        updated_at (datetime): Timestamp of last modification.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=300)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    needs_revision = models.BooleanField(default=False)
    editor_feedback = models.TextField(blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns:
            str: Title of the article.
        """
        return self.title


class Newsletter(models.Model):
    """
    A recurring editorial piece authored independently by a journalist.

    Attributes:
        title (str): Newsletter headline.
        content (str): Full body of the newsletter.
        author (CustomUser): Journalist who composed the newsletter.
        publisher (Publisher): Organization under which it was published.
        created_at (datetime): Timestamp of creation.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns:
            str: Title of the newsletter.
        """
        return self.title
