from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
	path('', views.FormListView.as_view(), name='form_list'),
	path('create', views.UserFormCreate.as_view(), name='form_create'),
	path('form_submit/<int:form_id>', views.form_submit, name='form_submit'),
	path('form_submissions/<int:form_id>', views.form_submissions, 
		name='form_submissions'),
]