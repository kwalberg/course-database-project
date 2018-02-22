from django.urls import path
from . import views


urlpatterns = [
    path('', views.search, name='search'),
    path('results/', views.search_results, name='results'),
    path('class/<str:class_name>/', views.class_page, name='class'),
    path('login/', views.login, name='login')
]