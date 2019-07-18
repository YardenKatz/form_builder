import json
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.forms import ModelForm
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import UserForm, FormField, Submissions, FieldSubmission
from django.http import HttpResponse #TODO: delete
import datetime
# from phonenumber_field.formfields import PhoneNumberField
#from phone_field import PhoneField


class FormFieldsForm(ModelForm):

	class Meta:
		model = FormField
		exclude = ()

FormFieldFormSet = inlineformset_factory(
	UserForm, FormField, extra=1, form=FormFieldsForm, 
	fields=['input_name', 'label', 'data_type'], can_delete=True,
	)


class UserFormForm(ModelForm):

    class Meta:
        model = UserForm
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(UserFormForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Fieldset('Add fields',
                    Formset('form_fields')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )


# class FieldSubmissionForm(ModelForm):

# 	class Meta:
# 		model = FieldSubmission
# 		fields = ['data', 'submission_id']
	

# 	def __init__(self, *args, **kwargs):
# 		form_id = kwargs.pop('form_id')
# 		# submissions = kwargs.pop('submissions')
# 		# submission_id = kwargs.pop('submission_id')
# 		super().__init__(*args, **kwargs)

# 		widgets = {
# 			# TODO: for each widget: attrs={
#             # "class": "form-control",
#             # "placeholder": "Your Name"
#         # }
# 			'TX': forms.CharField(max_length=100),
# 			'EML': forms.EmailField(),
# 			'NUM': forms.IntegerField(),
# 		}

# 		submissions = Submissions.objects.filter(
# 			form_id=form_id).order_by('-submission_id')
# 		try:
# 			submission_id = 1
# 		except ObjectDoesNotExist:
# 			max_id = submissions[0].submission_id
# 			submission_id = max_id + 1

# 		fields = FormField.objects.filter(form_id=form_id)
# 		for field in fields:
# 			input_name = field.input_name
# 			data_type = field.data_type
# 			label = field.label
# 			self.fields['form_id'] = form_id
# 			self.fields['submission_id'] = submission_id
# 			self.fields['field_id'] = field.id
# 			self.fields['data'] = widgets.get(data_type)
# 			# self.fields['data'].label = label
			
# 			try:
# 				submission = Submissions.objects.get(field_id = field.id)
# 				self.initial['data'] = json.loads(submission.data)
				
# 			except ObjectDoesNotExist:
# 				self.initial['data'] = ''
			
# 	def clean(self):
# 		# a list of tuples in the form of (field_id, data)
# 		ret_fields = []
# 		fields = FormField.objects.filter(self.form_id)
# 		for field in fields:
# 			ret_fields.append(
# 				(field.id, self.cleaned_data[field.input_name])
# 				)
# 		self.cleaned_data['fields'] = ret_fields
		

# 	def save(self):
# 		# submission = self.instance
# 		# submission.form_id = self.cleaned_data['form_id']
# 		# submission.field_id = self.cleaned_data['field_id']
# 		# submission.submission_id = self.cleaned_data['submission_id']

# 		for field in self.cleaned_data['fields']:
# 			Submissions.objects.create(
# 				form_id=self.cleaned_data['form_id'],
# 				submission_id=self.cleaned_data['submission_id'],
# 				# corresponding to the form of clean().ret_fields
# 				field_id=field[0],
# 				data=json.dumps(field[1])
# 			)


# 	def get_data_fields(self):
# 		''' using yield for returning generator and saving memory space, 
# 		as data will be read only once  '''

# 		i = 0
# 		# for field_name in self.fields:
# 		# 	if field_name == 'data':
# 		# 		# yield self[field_name]
# 		# 		i+=1
# 		# 		yield i		
# 		# submission_id = self.fields['submission_id']
# 		form_id = self.fields['form_id']
# 		fields = FormField.objects.filter(form_id=form_id)
# 		for field in fields:
# 			current_field = Submissions.objects.get(form_id=form_id, field_id=field.id)
# 			yield self[current_field]
# 			i+=1
# 			# yield i
	


class SubmissionsForm(ModelForm):

	class Meta:
		model = Submissions
		fields = '__all__'
		# exclude = ('user_form', 'submission_id')

	def __init__(self, *args, **kwargs):
		user_form = kwargs.pop('user_form')
		self.user_form = user_form
		super().__init__(*args, **kwargs)
		# self.fields['user_form'] = UserForm.objects.get(id=user_form.id)
		# submission_id = kwargs.pop('submission_id') #TODO: get from view

		widgets = {
			# TODO: for each widget: attrs={
            # "class": "form-control",
            # "placeholder": "Your Name"
        # }
			'TX': forms.CharField(max_length=100),
			'EML': forms.EmailField(),
			'NUM': forms.IntegerField(),
			'DAT': forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.datetime.now())#, label='Date'),
			# 'TEL': PhoneNumberField()
			# 'COL': 
		}
		fields = FormField.objects.filter(form_id=user_form)
		# i = 0
		for field in fields:
			# creates form fields corresponding to FormFields
			# i += 1
			# field_name = 'field_%s' % (i, )
			field_name = 'field_%s' % (field.input_name, )
			data_type = field.data_type
			label = field.label
			
			self.fields[field_name] = widgets.get(data_type)
			self.fields[field_name].widget.label = label
				
			try:
				submissions = FieldSubmission.objects.filter(
					submission=self.instance
				)
				self.initial[field_name] = json.loads(submissions[field.pk].data) 
			except IndexError:
				self.initial[field_name] = ''
		self.initial['user_form'] = user_form
			
	def clean(self):
		''' creates a list of tuples in the form of (field_id, data) in 
			self.cleaned_data['fields'] '''
		
		ret_fields = []
		# fields = FormField.objects.filter(form_id=self.instance.user_form)
		# i = 0
		# for field in fields:
		# 	i += 1
		# 	field_name = 'field_%s' % (i, )
		# 	ret_fields.append(
		# 		(field.id, self.cleaned_data[field_name])
		# 		)
		# self.cleaned_data['fields'] = ret_fields

		i = 0
		fields = FormField.objects.filter(form_id=self.user_form)
		for field in fields:
			i += 1
			# ret_fields.append(i)
			field_name = 'field_%s' % (field.input_name)
			ret_fields.append((field, self.cleaned_data[field_name]))
		self.cleaned_data['fields'] = ret_fields
		

	def save(self, *args, **kwargs):
		''' create a new FieldSubmission object for each form field '''

		user_form = kwargs.pop('user_form')
		submission_id = kwargs.pop('submission_id')
		submission = self.instance
		submission.user_form = user_form
		submission.submission_id = submission_id
		submission.save()
		# submission.user_form = self.cleaned_data['user_form']
		# submission.field_set.all().delete()


		# Submissions.objects.create(
		# 	user_form=user_form,
		# 	submission_id=submission_id
		# )

		for field in self.cleaned_data['fields']:
		# 	field_submisssion = FieldSubmission(
		# 		submission=submission,
		# 		# corresponding to the form of clean().ret_fields
		# 		field_id=field[0],
		# 		data=json.dumps(field[1])
		# 	)
		# 	field_submisssion.save()
			FieldSubmission.objects.create(
				submission=submission,
				# corresponding to the form of clean().ret_fields
				field_id=field[0],
				data=json.dumps(field[1], cls=DjangoJSONEncoder)
			)
		
		# return submission
		# return redirect('form_list.html')


	def get_data_fields(self):
		''' using yield for returning generator and saving memory space, 
		as data will be read only once  '''

		for field_name in self.fields:
			if field_name.startswith('field_'):
				yield self[field_name]
