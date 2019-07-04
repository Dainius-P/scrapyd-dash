from django.urls import path

from . import views

urlpatterns = [
	path('api/v3/servers/', views.ServerList.as_view()),
	path('api/v3/servers/<int:pk>', views.ServerDetails.as_view()),

	path('api/v3/tasks/', views.TaskList.as_view()),
	path('api/v3/tasks/<slug:pk>', views.TaskDetails.as_view()),
]