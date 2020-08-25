from django.forms import Form, FileField, ValidationError, FileInput
from django.core.validators import FileExtensionValidator


class JobForm(Form):

    file = FileField(label='Excel file', required=True,
                     validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'csv'])],
                     widget=FileInput())








