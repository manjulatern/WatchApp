from django.urls import path
from goldapp import views

urlpatterns = [
		path("", views.home),
		path("updateConfig/",views.update_configuration)
]