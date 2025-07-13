"""
Forms for user creation, newsletter submission, and publisher management.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Newsletter, Publisher


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user with a role.

    Fields:
        - username
        - email
        - role (reader, journalist, editor)
        - password1
        - password2
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')


class NewsletterForm(forms.ModelForm):
    """
    Form used by journalists to create a newsletter.

    Includes title, content, and publisher selection.
    """
    class Meta:
        model = Newsletter
        fields = ('title', 'content', 'publisher')


class PublisherForm(forms.ModelForm):
    """
    Form for creating a new publisher organization.
    """
    class Meta:
        model = Publisher
        fields = ['name']
