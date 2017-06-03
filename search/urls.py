from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search_town, name='search_town'),

]