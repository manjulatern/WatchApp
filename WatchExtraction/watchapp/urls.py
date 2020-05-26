from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^watch/$', views.index, name='index'),
	url(r'^watch/lot/(?P<lot>[A-Za-z0-9]+)/$', views.lot_details, name='lot_details'),
	url(r'^jobs/(?P<job>[0-9]+)/$', views.job_details, name='job_details'),
	url(r'^jobs/kill/(?P<job>[0-9]+)/$', views.job_kill, name='job_kill'),
	url(r'^jobs/run/(?P<job>[0-9]+)/$', views.job_run, name='job_run'),
	url(r'^watch/advsearch/$', views.advsearch, name='advsearch'),
	url(r'^jobs/$', views.allJobs, name='allJobs'),
	url(r'^jobs-progress/(?P<job>[0-9]+)/$', views.job_progress_details, name='job_progress_details'),
	url(r'^jobs/complete/$', views.completedJobs, name='completedJobs'),
	url(r'^jobs/failed/$', views.failedJobs, name='failedJobs'),
	url(r'^jobs/add$', views.addJobs, name='addJobs'),
	url(r'^jobs/create$', views.createJobs, name='createJobs'),
	url(r'^setup$', views.setup, name='setup'),
	url(r'^houses$', views.houses, name='houses'),
	url(r'^houses/(?P<house>[0-9]+)/$', views.house_details, name='house_details'),
	url(r'^jobs/runURL/(?P<auction>[0-9]+)/$', views.auction_run, name='auction_run'),
]