from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/cityPolygon$', views.search_cityPolygon, name='getPolygon'),
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^search/cityFilterMarker$', views.search_marker, name='getMarker'),
    url(r'^search/cityFilterIntersects$', views.search_filter, name='getIntersection'),
    url(r'^search/OpenData$', views.opendata_von_stadtteil, name='getOpenData')

]