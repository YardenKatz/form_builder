from django.db import models
from django.contrib.auth.models import User
# from django.forms import ModelForm
# from django import forms

FIELD_TYPES = [
	('TX', 'Text'),
	('EML', 'Email'),
	('NUM', 'Number'),
]

# class FormList(models.Model):
# 	form_id = models.PositiveSmallIntegerField()
# 	name = models.CharField(max_length=50)
# 	submissions = models.PositiveSmallIntegerField()

# 	def __str__(self):
# 		return self.name
	

class UserForm(models.Model):
	# sub_id = models.PositiveSmallIntegerField() - simply use id
	# form_id = models.ForeignKey(FormList, on_delete=models.CASCADE)
	
	# def __str__(self):
	# 	return self.form_id.name

	name = models.CharField(max_length=50)
	# submissions = models.PositiveSmallIntegerField()
	# created_by = models.ForeignKey(User,
		# related_name='userforms', blank=True, null=True, 
		# on_delete=models.SET_NULL)


	def __str__(self):
		return self.name
	

class FormField(models.Model):
	form_id = models.ForeignKey(UserForm, related_name='has_fields',
		on_delete=models.CASCADE)
	# field_id = models.IntegerField()
	label = models.CharField(max_length=30)
	input_name = models.CharField(max_length=30)
	data_type = models.CharField(max_length=3, choices=FIELD_TYPES)
	# data = models.TextField(blank=True)

	def __str__(self):
		return self.label


class Submissions(models.Model):
	user_form = models.ForeignKey(UserForm, related_name='has_submission',
		on_delete=models.CASCADE, null=True)
	submission_id = models.PositiveIntegerField() 

	def __str__(self):
		return self.submission_id
	

class FieldSubmission(models.Model):
	# form_id = models.ForeignKey(UserForm, related_name='has_submisssions',
	# 	on_delete=models.CASCADE)
	# submission_id = models.PositiveIntegerField() 
	submission = models.ForeignKey(Submissions, on_delete=models.CASCADE)
	field_id = models.OneToOneField(FormField, on_delete=models.CASCADE)
	data = models.TextField()

	def __str__(self):
		return self.field_id
	
#class FormWizard(forms.ModelForm):
#	class Meta:
#		model = UserForm
#
#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)
#		form_fields = FormField.objects.filter(
#			form_id=self.instance
#		)
#		# display existing fields with inserted data
#		for i in range(len(form_fields) + 1):
#			# field_name = 'form_field_%s' % (i,)
#			self.fields['label'] = forms.CharField(
#				max_length=30, 
#				required=False
#			)
#			try:
#				self.initial['label'] = form_fields[i].label
#			except IndexError:
#				self.initial['label'] = ''
#
#			self.fields['input_name'] = forms.CharField(
#				max_length=30, 
#				required=False
#			)
#			try:
#				self.initial['input_name'] = form_fields[i].input_name
#			except IndexError:
#				self.initial['input_name'] = ''
#
#			self.fields['data_type'] = forms.ChoiceField(
#				choices=FIELD_TYPES, 
#				label='Data Type',
#				max_length=3, 
#				required=False
#			)
#			try:
#				self.initial['data_type'] = form_fields[i].data_type
#			except IndexError:
#				self.initial['data_type'] = ''
#
#		# create an extra blank field row
#		field_id = 'form_field_%s' % (i + 1,)
#		self.fields[field_name] = forms.CharField(required=False) # should have types choice
#
#	def clean(self):
#		form_fields = set()
#		i = 0
#		field_name = 'form_field_%s' % (i,)
#		while self.cleaned_data.get(field_name):
#			form_field = self.cleaned_data[field_name]
#			if form_field in form_fields:
#				self.add_error(field_name, 'Duplicate')
#			else:
#				form_fields.add(form_field)
#			i += 1
#			field_name = 'form_field_%s' % (i,)
#		self.cleaned_data['form_fields'] = form_fields
#
#	def save(self):
#		form_id = self.instance
#
#		form_id.form_field_set.all().delete()
#		for form_field in self.cleaned_data['form_fields']:
#			FormField.objects.create(
#				form_id=form_id,
#				form_field=form_field,
#			)
#