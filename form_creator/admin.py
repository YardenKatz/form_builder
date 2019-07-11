from django.contrib import admin
from .models import UserForm, FormField #,FormList

# admin.site.register(FormList)
admin.site.register(UserForm)
admin.site.register(FormField)