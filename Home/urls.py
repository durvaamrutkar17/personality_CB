from django.urls import path
from . import views

urlpatterns = [
    path('/', views.index, name='index'),
    path('/submit/', views.submit, name='submit'),
    path('/feedback/', views.feedback_view, name='feedback'),
]
