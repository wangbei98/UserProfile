from django.urls import path

from . import views

urlpatterns = [
	path(r'register/',views.register,name='register-view')
]