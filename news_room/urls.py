from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Core & auth
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='news_room/password_reset.html',
        email_template_name='news_room/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='news_room/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='news_room/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='news_room/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Articles
    path('articles/', views.article_list_view, name='article_list'),
    path('article/<int:article_id>/', views.view_article_view, name='view_article'),
    path('create-article/', views.create_article_view, name='create_article'),
    path('edit-article/<int:article_id>/', views.edit_article_view, name='edit_article'),
    path('journalist-feedback/', views.journalist_feedback_view, name='journalist_feedback'),
    path('review-articles/', views.review_articles_view, name='review_articles'),
    path('approve-article/<int:article_id>/', views.approve_article_view, name='approve_article'),
    path('request-revision/<int:article_id>/', views.request_revision_view, name='request_revision'),
    path('create-publisher/', views.create_publisher_view, name='create_publisher'),


    # Subscriptions
    path('subscribe/journalist/<int:journalist_id>/', views.subscribe_journalist_view,
         name='subscribe_journalist'),
    path('subscribe/publisher/<int:publisher_id>/', views.subscribe_publisher_view,
         name='subscribe_publisher'),

    # Directory
    path('directory/', views.directory_view, name='directory'),

    # Newsletters
    path('newsletters/', views.newsletter_list_view, name='newsletter_list'),
    path('newsletter/<int:newsletter_id>/', views.view_newsletter_view,
         name='view_newsletter'),
    path('create-newsletter/', views.create_newsletter_view, name='create_newsletter'),
    path(
    'my-newsletters/',
    views.my_newsletters_view,
    name='my_newsletters'
    ),


    # API endpoints
    path('api/publisher-articles/', views.PublisherArticlesAPIView.as_view(),
         name='publisher_articles_api'),
    path('api/journalist-articles/', views.JournalistArticlesAPIView.as_view(),
         name='journalist_articles_api'),
    path('api/newsletters/', views.NewsletterListAPIView.as_view(),
         name='newsletter_api'),

    # OAuth callback
    path('twitter/callback/', views.twitter_callback_view, name='twitter_callback'),
]
