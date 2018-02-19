from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('results/<str:query>/', views.search_results, name='results'),
    path('class/<str:class_name>/', views.class_page, name='class')
]