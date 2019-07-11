from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	# path('', views.index, name='form_create'),
	path('<int:form_id>', views.index, name='index'),
	path('', views.FormListView.as_view(), name='form_list'),
	path('create', views.UserFormCreate.as_view(), name='form_create'),
	path('form_confirm', views.formSubmitConfirm, name='form_submitted')
]