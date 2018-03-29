from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django_filters.views import FilterView


urlpatterns = [
    url('search/', FilterView.as_view(template_name='search/user_list.html'), name='search'),
    path('', views.search, name='search'),
    path('results/', views.search_results, name='results'),
    path('class/<str:class_name>/', views.class_page, name='class'),
    url(r'^login/$', auth_views.login, {"template_name": "Login.html"}),
    path('rate/<str:class_name>/', views.rate_course, name='rate'),
    path('submit_review/<str:class_name>/', views.submit_review, name='submit_review'),
    url('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls'))
]