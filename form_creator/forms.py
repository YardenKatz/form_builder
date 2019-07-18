import json
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.forms import ModelForm
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import UserForm, FormField, Submissions, FieldSubmission


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


class SubmissionsForm(ModelForm):

	class Meta:
		model = Submissions
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		user_form = kwargs.pop('user_form')
		self.user_form = user_form
		super().__init__(*args, **kwargs)

		widgets = {
			'TX': forms.CharField(max_length=100),
			'EML': forms.EmailField(),
			'NUM': forms.IntegerField(),
			'DAT': forms.DateField(widget=forms.SelectDateWidget(
				years=range(1980, 2020))),
		}

		fields = FormField.objects.filter(form_id=user_form)
		for field in fields:
			field_name = 'field_%s' % (field.input_name, )
			data_type = field.data_type
			label = field.label
			self.fields[field_name] = widgets.get(data_type)
			self.fields[field_name].label = label
				
			try:
				submissions = FieldSubmission.objects.filter(
					submission=self.instance)
				self.initial[field_name] = json.loads(
					submissions[field.pk].data) 
			except IndexError:
				self.initial[field_name] = ''
		self.initial['user_form'] = user_form
			
	def clean(self):
		''' creates a list of tuples in the form of (field_id, data) in 
			self.cleaned_data['fields'] '''
		
		ret_fields = []
		i = 0
		fields = FormField.objects.filter(form_id=self.user_form)
		for field in fields:
			i += 1
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

		for field in self.cleaned_data['fields']:
			FieldSubmission.objects.create(
				submission=submission,
				field_id=field[0],
				data=json.dumps(field[1], cls=DjangoJSONEncoder)
			)

	def get_data_fields(self):
		''' using yield for returning generator and saving memory space, 
		as data will be read only once  '''

		for field_name in self.fields:
			if field_name.startswith('field_'):
				yield self[field_name]
