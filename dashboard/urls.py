from django.urls import path

from . import views

urlpatterns = [
	path('', views.index_view, name="index"),
]

from .operations.check_servers import CheckServers

c = CheckServers()
c.check_servers()