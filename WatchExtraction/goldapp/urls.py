from django.urls import path,re_path
from goldapp import views

urlpatterns = [
		path("", views.home),
		path("updateConfig/",views.update_configuration),
		re_path(r'^getdata_json/(?P<percentage>\d+(?:\.\d+)?)/(?P<goldgram>\d+(?:\.\d+)?)', views.myajaxview, name='getdata_json')

]