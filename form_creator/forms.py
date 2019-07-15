import json
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import UserForm, FormField, Submission


class FormFieldsForm(ModelForm):

	class Meta:
		model = FormField
		exclude = ()

FormFieldFormSet = inlineformset_factory(
	UserForm, FormField, extra=1, form=FormFieldsForm, 
	fields=['label', 'input_name', 'data_type'], can_delete=True,
	)


class UserFormForm(ModelForm):

    class Meta:
        model = UserForm
        exclude = ['submissions', 'created_by']

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


class SubmissionForm(ModelForm):

	class Meta:
		model = Submission
		fields = ['data', 'submission_id']
	

	def __init__(self, *args, **kwargs):
		form_id = kwargs.pop('form_id')
		# submissions = kwargs.pop('submissions')
		# submission_id = kwargs.pop('submission_id')
		super().__init__(*args, **kwargs)

		widgets = {
			# TODO: for each widget: attrs={
            # "class": "form-control",
            # "placeholder": "Your Name"
        # }
			'TX': forms.CharField(max_length=100),
			'EML': forms.EmailField(),
			'NUM': forms.IntegerField(),
		}

		submissions = Submission.objects.filter(
			form_id=form_id).order_by('-submission_id')
		try:
			submission_id = 1
		except ObjectDoesNotExist:
			max_id = submissions[0].submission_id
			submission_id = max_id + 1

		fields = FormField.objects.filter(form_id=form_id)
		for field in fields:
			input_name = field.input_name
			data_type = field.data_type
			label = field.label
			self.fields['form_id'] = form_id
			self.fields['submission_id'] = submission_id
			self.fields['field_id'] = field.id
			self.fields['data'] = widgets.get(data_type)
			# self.fields['data'].label = label
			
			try:
				submission = Submission.objects.get(field_id = field.id)
				self.initial['data'] = json.loads(submission.data)
				
			except ObjectDoesNotExist:
				self.initial['data'] = ''
			
	def clean(self):
		# a list of tuples in the form of (field_id, data)
		ret_fields = []
		fields = FormField.objects.filter(self.form_id)
		for field in fields:
			ret_fields.append(
				(field.id, self.cleaned_data[field.input_name])
				)
		self.cleaned_data['fields'] = ret_fields
		

	def save(self):
		# submission = self.instance
		# submission.form_id = self.cleaned_data['form_id']
		# submission.field_id = self.cleaned_data['field_id']
		# submission.submission_id = self.cleaned_data['submission_id']

		for field in self.cleaned_data['fields']:
			Submission.objects.create(
				form_id=self.cleaned_data['form_id'],
				submission_id=self.cleaned_data['submission_id'],
				# corresponding to the form of clean().ret_fields
				field_id=field[0],
				data=json.dumps(field[1])
			)


	def get_data_fields(self):
		''' using yield for returning generator and saving memory space, 
		as data will be read only once  '''

		for field_name in self.fields:
			if field_name == 'data':
				yield self[field_name]
	
