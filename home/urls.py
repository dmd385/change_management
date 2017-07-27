from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^logout/', views.logOut, name='logout'),
    url(r'^', views.log_in, name='log_in'),
]