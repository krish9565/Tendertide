from django.urls import path
from . import views

app_name = 'tenders'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('news/', views.news, name='news'),
    path('tenders/', views.tender_list, name='tender_list'),
    path('tenders/<int:pk>/', views.tender_detail, name='tender_detail'),
    path('tenders/create/', views.create_tender, name='create_tender'),
    path('tenders/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
]