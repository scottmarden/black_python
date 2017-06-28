from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^travels$', views.success),
	url(r'^travels/add$', views.add_trip),
	url(r'^travels/destination/(?P<id>\d+$)', views.trip_details),
	url(r'^new_trip$', views.new_trip),
	url(r'^join_trip$', views.join_trip),
	url(r'^logout$', views.logout),
]
