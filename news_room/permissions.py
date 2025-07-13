"""
Role setup script for creating base user groups and assigning permissions.

This script can be run during initial migration or seeding to ensure
Reader, Editor, and Journalist groups have appropriate model-level access.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Article, Newsletter


def create_roles():
    """
    Define role-based groups and assign Django model permissions.

    Groups created:
        - Reader: view access only
        - Editor: view, change, delete access
        - Journalist: full CRUD access

    Permissions cover Article and Newsletter models.
    """
    reader, _ = Group.objects.get_or_create(name='Reader')
    editor, _ = Group.objects.get_or_create(name='Editor')
    journalist, _ = Group.objects.get_or_create(name='Journalist')

    article_ct = ContentType.objects.get_for_model(Article)
    newsletter_ct = ContentType.objects.get_for_model(Newsletter)

    reader.permissions.set(Permission.objects.filter(codename__in=[
        'view_article', 'view_newsletter'
    ]))

    editor.permissions.set(Permission.objects.filter(codename__in=[
        'view_article', 'change_article', 'delete_article',
        'view_newsletter', 'change_newsletter', 'delete_newsletter'
    ]))

    journalist.permissions.set(Permission.objects.filter(codename__in=[
        'add_article', 'change_article', 'view_article', 'delete_article',
        'add_newsletter', 'change_newsletter', 'view_newsletter', 'delete_newsletter'
    ]))
