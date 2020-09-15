from django.forms import Form, FileField, FileInput


class JobForm(Form):

    file = FileField(label='Excel file', required=True,
                     widget=FileInput())








