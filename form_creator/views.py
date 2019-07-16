from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView #TODO: remove unnecessary 
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import modelformset_factory, inlineformset_factory # TODO: remove unnecesary 
from django.http import HttpResponse #TODO: delete

# def index(request, form_id):
# 	userform = UserForm.objects.get(pk=id)#(pk=form_id)
# 	# FieldFormset = modelformset_factory(FormField, fields=(
# 		# 'label', 
# 		# 'input_name',
# 		# 'data_type',
# 		# ))
# 	FieldFormset = inlineformset_factory(UserForm, FormField, extra=1, fields=(
# 		'label','input_name','data_type',))

# 	if request.method == 'POST':
# 		# formset = FieldFormset(request.POST, queryset=FormField.objects.filter(form_id=userform))	
# 		formset = FieldFormset(request.POST, instance=userform)
# 		if formset.is_valid():
# 			formset.save()
# 			# instances = formset.save(commit=False)
# 			# for instance in instances:
# 			# 	instance.form_id = userform
# 			# 	instance.save()

# 			return redirect('index', form_id=userform.id)

# 	# formset = FieldFormset(queryset=FormField.objects.filter(form_id=userform))
# 	formset = FieldFormset(instance=userform)

# 	return render(request, 'index.html', {'formset': formset})


# def sample(request):
# 	return HttpResponse('Index View...')


# def formSubmitConfirm(request):
# 	return HttpResponse('Your Form Was Submitted Succesfully')


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


# def form_submit(request, form_id):
# 	userform = UserForm.objects.get(pk=form_id)
# 	# fields = FormField.objects.filter(form_id=form_id)
# 	# submissions = Submission.objects.filter(form_id=form_id).order_by('-submission_id')
# 	# if not submissions:
# 	# 	submission_id = 1
# 	# else:
# 	# 	max_id = submissions[0].submission_id
# 	# 	submission_id = max_id + 1

# 	form = SubmissionForm(form_id=userform)#, submission_id=submission_id)
# 	if request.method == 'POST':
# 		form = SubmissionForm(
# 			request.POST, form_id=userform)#, submission_id=submission_id)
# 		if form.is_valid():
# 			submission = Submission(
# 				# form_id=userform,
# 				# submission_id=submission_id,
# 				# field_id=form.cleaned_data['field_id'],
# 				# data=form.cleaned_data['data']
# 			)
# 			submission.save()
		
# 	context = {
# 		'name': userform.name, #TODO: remove if unnecessary
# 		'form': form
# 	}

# 	return render(request, 'form_submit.html', context)


def form_submit(request, form_id):
	userform = UserForm.objects.get(pk=form_id)
	submissions = Submissions.objects.filter(user_form=userform).order_by('-submission_id')
	if not submissions:
		submission_id = 1
	else:
		max_id = submissions[0].submission_id
		submission_id = max_id + 1

	form = SubmissionsForm(user_form=userform)#, 
		# initial={'user_form': userform, 'submission_id': submission_id})
	if request.method == 'POST':
		form = SubmissionsForm(
			request.POST, user_form=userform)#, initial={'user_form': userform, 'submission_id': submission_id})
		if form.is_valid():
			submission = form.save(commit=False, user_form=userform, submission_id=submission_id)
			submission.user_form=userform
			submission.submission_id=submission_id
			submission.save()
			new_submission = Submissions(
				user_form=userform,
				submission_id=submission_id
			)
			new_submission.save()
			return redirect('/form_builder/')

	context = {
		# TODO: delete unused context
		'userform': userform,
		'submission_id': submission_id,
		'name': userform.name,
		'form': form
	}

	return render(request, 'form_submit.html', context)


def form_submissions(request, form_id):
	
	context = {
	# 	'userform': userform,
	# 	'fields': fields,
	# 	'submissions': submissions,
	}

	return render(request, 'form_submissions.html', context)







