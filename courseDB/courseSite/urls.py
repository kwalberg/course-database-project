from django.urls import path
from . import views
from django.conf.urls import url
from django_filters.views import FilterView


urlpatterns = [
    url(r'^search/$', FilterView.as_view(template_name='search/user_list.html'), name='search'),
    path('', views.search, name='search'),
    path('results/', views.search_results, name='results'),
    path('class/<str:class_name>/', views.class_page, name='class'),
    path('login/', views.login, name='login'),
    path('rate/<str:class_name>/', views.rate_course, name='rate'),
    path('submit_review/<str:class_name>/', views.submit_review, name='submit_review')
]