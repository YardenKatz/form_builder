from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import UserForm, FormField


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

