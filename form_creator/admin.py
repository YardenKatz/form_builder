from django.contrib import admin
from .models import UserForm, FormField #,FormList

class UserformAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)


class FormfieldAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

# admin.site.register(FormList)
admin.site.register(UserForm, UserformAdmin)
admin.site.register(FormField, FormfieldAdmin)