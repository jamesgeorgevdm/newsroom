"""
Views for NewsRoom application.

Handles authentication, article and newsletter management, subscriptions,
publisher creation, directory browsing, and REST API endpoints.
Role-based access is enforced for readers, journalists, and editors.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework import generics, permissions

from .models import Article, Publisher, CustomUser, Newsletter
from .forms import CustomUserCreationForm, NewsletterForm, PublisherForm
from .serializers import ArticleSerializer, NewsletterSerializer


# ---------- Helper Role Checks ----------

def is_journalist(user):
    """
    Check if the user has a journalist role.

    Parameters:
        user (CustomUser): Current user object.

    Returns:
        bool: True if user is a journalist, False otherwise.
    """
    return user.role == 'journalist'


def is_editor(user):
    """
    Check if the user has an editor role.

    Parameters:
        user (CustomUser): Current user object.

    Returns:
        bool: True if user is an editor, False otherwise.
    """
    return user.role == 'editor'


# ---------- Authentication Views ----------

def register_view(request):
    """
    Register a new user using the custom user creation form.

    Parameters:
        request (HttpRequest): The request containing form data.

    Returns:
        HttpResponse: Rendered registration form or redirect to dashboard.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'news_room/register.html', {'form': form})


def login_view(request):
    """
    Authenticate and log in an existing user.

    Parameters:
        request (HttpRequest): Login credentials submitted via form.

    Returns:
        HttpResponse: Rendered login form or redirect to dashboard.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'news_room/login.html', {'form': form})


def logout_view(request):
    """
    Log out the current user and redirect to login page.

    Parameters:
        request (HttpRequest): Logout trigger.

    Returns:
        HttpResponse: Redirect to login view.
    """
    logout(request)
    return redirect('login')


# ---------- Dashboard ----------

@login_required
def dashboard_view(request):
    """
    Render dashboard view.

    Readers and journalists see all approved articles and newsletters.
    Editors see an empty view.

    Parameters:
        request (HttpRequest): Current user request.

    Returns:
        HttpResponse: Rendered dashboard page.
    """
    show = request.user.role in ['reader', 'journalist']
    articles = Article.objects.filter(approved=True) if show else []
    newsletters = Newsletter.objects.all() if show else []
    return render(request, 'news_room/dashboard.html', {
        'articles': articles,
        'newsletters': newsletters,
    })


# ---------- Article Views ----------

@login_required
def article_list_view(request):
    """
    Display all approved articles.

    Returns:
        HttpResponse: Rendered article list.
    """
    articles = Article.objects.filter(approved=True)
    return render(request, 'news_room/article_list.html', {'articles': articles})


@login_required
def view_article_view(request, article_id):
    """
    Display details of a single article.

    Parameters:
        article_id (int): ID of the article.

    Returns:
        HttpResponse: Rendered article view.
    """
    if request.user.role == 'editor':
        article = get_object_or_404(Article, id=article_id)
    else:
        article = get_object_or_404(Article, id=article_id, approved=True)
    return render(request, 'news_room/view_article.html', {'article': article})


@login_required
@user_passes_test(is_journalist)
def create_article_view(request):
    """
    Allow journalists to create and submit an article.

    Returns:
        HttpResponse: Article form page or redirect to dashboard.
    """
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        content = request.POST['content']
        publisher = get_object_or_404(Publisher, id=request.POST['publisher_id'])
        article = Article.objects.create(
            title=title,
            description=description,
            content=content,
            author=request.user,
            publisher=publisher
        )
        request.user.published_articles.add(article)
        messages.success(request, 'Article submitted for approval.')
        return redirect('dashboard')
    publishers = Publisher.objects.all()
    return render(request, 'news_room/create_article.html', {'publishers': publishers})


@login_required
@user_passes_test(is_journalist)
def edit_article_view(request, article_id):
    """
    Allow journalists to revise articles flagged for revision.

    Parameters:
        article_id (int): ID of the article to edit.

    Returns:
        HttpResponse: Article editing page or redirect.
    """
    article = get_object_or_404(Article, id=article_id)
    if article.author != request.user or not article.needs_revision:
        return HttpResponseForbidden("You are not allowed to edit this article.")
    if request.method == 'POST':
        article.title = request.POST.get('title', article.title)
        article.content = request.POST.get('content', article.content)
        article.needs_revision = False
        article.approved = False
        article.editor_feedback = ''
        article.save()
        request.user.published_articles.add(article)
        messages.success(request, 'Article resubmitted for review.')
        return redirect('journalist_feedback')
    return render(request, 'news_room/edit_article.html', {'article': article})


# ---------- Editor Actions ----------

@login_required
@user_passes_test(is_editor)
def review_articles_view(request):
    """
    Display all articles needing approval or revision.

    Returns:
        HttpResponse: Review articles view.
    """
    pending = Article.objects.filter(approved=False)
    flagged = Article.objects.filter(needs_revision=True)
    articles = (pending | flagged).distinct()
    return render(request, 'news_room/review_articles.html', {'articles': articles})


@login_required
@user_passes_test(is_editor)
def approve_article_view(request, article_id):
    """
    Approve an article and clear its revision flags.

    Parameters:
        article_id (int): ID of article to approve.

    Returns:
        HttpResponse: Redirect to review list.
    """
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.needs_revision = False
    article.editor_feedback = ''
    article.save()
    return redirect('review_articles')


@login_required
@user_passes_test(is_editor)
def request_revision_view(request, article_id):
    """
    Request revisions for an article with feedback.

    Parameters:
        article_id (int): ID of the article.

    Returns:
        HttpResponse: Feedback form or redirect.
    """
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.needs_revision = True
        article.approved = False
        article.editor_feedback = request.POST.get('feedback', '')
        article.save()
        return redirect('review_articles')
    return render(request, 'news_room/request_revision.html', {'article': article})


@login_required
@user_passes_test(is_editor)
def create_publisher_view(request):
    """
    Allow editors to create new publishers.

    Returns:
        HttpResponse: Publisher form or dashboard redirect.
    """
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            publisher.editors.add(request.user)
            return redirect('dashboard')
    else:
        form = PublisherForm()
    return render(request, 'news_room/create_publisher.html', {'form': form})


# ---------- Journalist Feedback ----------

@login_required
@user_passes_test(is_journalist)
def journalist_feedback_view(request):
    """
    Display all articles authored by the journalist.

    Returns:
        HttpResponse: Feedback dashboard.
    """
    articles = Article.objects.filter(author=request.user)
    return render(request, 'news_room/journalist_feedback.html', {'articles': articles})


# ---------- Newsletter Views ----------

@login_required
def newsletter_list_view(request):
    """
    Display all published newsletters.

    Returns:
        HttpResponse: Newsletter list view.
    """
    newsletters = Newsletter.objects.all()
    return render(request, 'news_room/newsletter_list.html', {'newsletters': newsletters})


@login_required
def view_newsletter_view(request, newsletter_id):
    """
    Display full content of a single newsletter.

    Parameters:
        newsletter_id (int): ID of the newsletter.

    Returns:
        HttpResponse: Newsletter detail view.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(request, 'news_room/view_newsletter.html', {'newsletter': newsletter})

@login_required
@user_passes_test(is_journalist)
def create_newsletter_view(request):
    """
    Allow journalists to compose and publish a newsletter.

    Parameters:
        request (HttpRequest): Form data containing newsletter fields.

    Returns:
        HttpResponse: Form page or redirect to dashboard on success.
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            request.user.published_newsletters.add(newsletter)
            messages.success(request, 'Newsletter published.')
            return redirect('dashboard')
    else:
        form = NewsletterForm()
    return render(request, 'news_room/create_newsletter.html', {'form': form})


@login_required
@user_passes_test(is_journalist)
def my_newsletters_view(request):
    """
    Display newsletters authored by the current journalist.

    Returns:
        HttpResponse: List of personal newsletters.
    """
    newsletters = Newsletter.objects.filter(author=request.user)
    return render(request, 'news_room/my_newsletters.html', {
        'newsletters': newsletters,
    })


# ---------- Subscription Views ----------

@login_required
def subscribe_journalist_view(request, journalist_id):
    """
    Allow readers to subscribe to a journalist.

    Parameters:
        journalist_id (int): ID of the journalist.

    Returns:
        HttpResponse: Redirect to previous page or article list.
    """
    if request.method == 'POST' and request.user.role == 'reader':
        journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')
        request.user.subscribed_journalists.add(journalist)
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'article_list'))


@login_required
def subscribe_publisher_view(request, publisher_id):
    """
    Allow readers to subscribe to a publisher.

    Parameters:
        publisher_id (int): ID of the publisher.

    Returns:
        HttpResponse: Redirect to previous page or article list.
    """
    if request.method == 'POST' and request.user.role == 'reader':
        publisher = get_object_or_404(Publisher, id=publisher_id)
        request.user.subscribed_publishers.add(publisher)
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'article_list'))

# ---------- Directory ----------

@login_required
def directory_view(request):
    """
    Display a directory listing all journalists and publishers.

    Returns:
        HttpResponse: Rendered directory page with grouped profiles.
    """
    journalists = CustomUser.objects.filter(role='journalist')
    publishers = Publisher.objects.all()
    return render(request, 'news_room/directory.html', {
        'journalists': journalists,
        'publishers': publishers,
    })


# ---------- REST API Views ----------

class PublisherArticlesAPIView(generics.ListAPIView):
    """
    API view returning articles from publishers the reader is subscribed to.

    Only includes articles that are approved.

    Attributes:
        serializer_class (Serializer): ArticleSerializer
        permission_classes (list): [IsAuthenticated]
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Query articles where publisher is in the reader's subscriptions.

        Returns:
            QuerySet: Filtered approved Article instances.
        """
        return Article.objects.filter(
            approved=True,
            publisher__in=self.request.user.subscribed_publishers.all()
        )


class JournalistArticlesAPIView(generics.ListAPIView):
    """
    API view returning articles from journalists the reader is subscribed to.

    Attributes:
        serializer_class (Serializer): ArticleSerializer
        permission_classes (list): [IsAuthenticated]
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Query articles where author is in the reader's subscriptions.

        Returns:
            QuerySet: Filtered approved Article instances.
        """
        return Article.objects.filter(
            approved=True,
            author__in=self.request.user.subscribed_journalists.all()
        )


class NewsletterListAPIView(generics.ListAPIView):
    """
    API view returning all newsletters visible to authenticated users.

    Attributes:
        serializer_class (Serializer): NewsletterSerializer
        permission_classes (list): [IsAuthenticated]
        queryset (QuerySet): All Newsletter objects
    """
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Newsletter.objects.all()


# ---------- OAuth Callback View ----------

def twitter_callback_view(request):
    """
    Capture the OAuth verifier from Twitter/X authorization flow.

    Used during terminal-based OAuth1 session when authenticating.

    Parameters:
        request (HttpRequest): Contains query param 'oauth_verifier'.

    Returns:
        HttpResponse: Verifier string for manual copy-paste into terminal.
    """
    verifier = request.GET.get('oauth_verifier')
    return HttpResponse(f"Copy this verifier into your terminal: <strong>{verifier}</strong>")
