from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/cityPolygon$', views.search_cityPolygon, name='getPolygon'),
    url(r'^$', views.search_town, name='search_town'),

]