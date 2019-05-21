from django.urls import path

from . import views

urlpatterns = [
	path(r'login/',views.login,name = 'login-view')
]