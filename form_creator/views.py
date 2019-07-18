from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView 
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory


class FormListView(ListView):
	context_object_name = 'form_list'
	queryset = UserForm.objects.all()
	template_name = 'form_list.html'

class UserFormCreate(CreateView):
	model = UserForm
	template_name = "form_create.html"
	form_class = UserFormForm
	success_url = None

	def get_context_data(self, **kwargs):
		context = super(UserFormCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['form_fields'] = FormFieldFormSet(self.request.POST)
		else:
			context['form_fields'] = FormFieldFormSet()
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		form_fields = context['form_fields']
		with transaction.atomic():
			form.instance.submissions = 0
			self.object = form.save()
			if form_fields.is_valid():
				form_fields.instance = self.object
				form_fields.save()
		return super(UserFormCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('form_list')


def form_submit(request, form_id):
	userform = UserForm.objects.get(pk=form_id)
	submissions = Submissions.objects.filter(user_form=userform).order_by('-submission_id')
	if not submissions:
		submission_id = 1
	else:
		max_id = submissions[0].submission_id
		submission_id = max_id + 1

	form = SubmissionsForm(user_form=userform)
	if request.method == 'POST':
		form = SubmissionsForm(
			request.POST, user_form=userform)
		if form.is_valid():
			form.save(user_form=userform, submission_id=submission_id)
			return redirect('/form_builder/')

	context = {
		'userform': userform,
		'submission_id': submission_id,
		'name': userform.name,
		'form': form
	}

	return render(request, 'form_submit.html', context)


def form_submissions(request, form_id):
	form_name = UserForm.objects.get(pk=form_id).name
	fields = FormField.objects.filter(form_id=form_id).order_by('input_name')
	submissions = Submissions.objects.filter(user_form=form_id).values_list()
	sumbission_fields_collection = {}
	i = 0
	for submission in submissions:
		i += 1
		submission_data = FieldSubmission.objects.filter(submission__user_form=form_id, submission=submission).values_list('data', flat=True).order_by('field_id__input_name')
		sumbission_fields_collection[i] = submission_data
		
	context = {
		'form_name': form_name,
		'fields': fields,
		'submissions': submissions,
		'submission_fields': sumbission_fields_collection
	}

	return render(request, 'form_submissions.html', context)


# def confirm(request):
# 	context = {}
# 	return render(request, 'confirm.html', context)


