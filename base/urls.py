from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('', views.step1_budget, name='step1_budget'),
    path('about/', views.about_page, name='about_page'),
]
