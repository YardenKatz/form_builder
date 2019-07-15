from django.contrib import admin
from .models import UserForm, FormField, Submissions, FieldSubmission #,FormList

class UserformAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)


class FormfieldAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)


class SubmissionsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)


class FieldSubmissionAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

# admin.site.register(FormList)
admin.site.register(UserForm, UserformAdmin)
admin.site.register(FormField, FormfieldAdmin)
admin.site.register(Submissions, SubmissionsAdmin)
admin.site.register(FieldSubmission, FieldSubmissionAdmin)