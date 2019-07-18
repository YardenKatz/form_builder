from django.db.models.signals import post_save
from django.db import models
from django.db.models import F


FIELD_TYPES = [
	('TX', 'Text'),
	('NUM', 'Number'),
	('DAT', 'Date'),
	('EML', 'Email'),
]
	

class UserForm(models.Model):

	name = models.CharField(max_length=50)
	submissions_counter = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.name
	

class FormField(models.Model):
	form_id = models.ForeignKey(UserForm, related_name='has_fields',
		on_delete=models.CASCADE)
	input_name = models.CharField(max_length=30)
	label = models.CharField(max_length=30)
	data_type = models.CharField(max_length=3, choices=FIELD_TYPES)

	def __str__(self):
		return self.label


class Submissions(models.Model):
	user_form = models.ForeignKey(UserForm, related_name='has_submission',
		on_delete=models.CASCADE, blank=True, null=True)
	submission_id = models.PositiveIntegerField(blank=True, null=True) 

	def __str__(self):
		return str(self.submission_id)
	

def update_submissions_count(sender, instance, created, **kwargs):
    if created:
        submission = instance
        user_form = submission.user_form
        user_form.submissions_counter = F('submissions_counter') + 1 
        user_form.save(update_fields=['submissions_counter']) 

post_save.connect(update_submissions_count, sender=Submissions)


class FieldSubmission(models.Model):
	submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name='field_set')
	field_id = models.ForeignKey(FormField, on_delete=models.CASCADE)
	data = models.TextField()