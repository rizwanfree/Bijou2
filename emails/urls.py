from django.urls import path
from .views import EmailListView, EmailDetailView, ComposeEmailView, fetch_emails, mark_email_read

urlpatterns = [
    path('', EmailListView.as_view(), name='email-list'),
    path('compose/', ComposeEmailView.as_view(), name='compose-email'),
    path('<int:pk>/', EmailDetailView.as_view(), name='email-detail'),
    path('fetch/', fetch_emails, name='fetch-emails'),
    path('<int:pk>/mark-read/', mark_email_read, name='mark-email-read'),
]