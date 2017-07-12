from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/cityPolygon$', views.search_cityPolygon, name='getPolygon'),
    url(r'^$', views.index, name='index'),
    url(r'^search/cityFilter', views.search_filter, name='getFilter')

]