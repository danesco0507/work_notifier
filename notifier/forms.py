__author__ = 'Daniel'

from django import forms
import os
from models import Work, Acceptance
from bootstrap3_datetime.widgets import DateTimePicker

IMPORT_FILE_TYPES = ['.xls', '.xlsx']

class WorkUploadForm(forms.ModelForm):
    input_excel = forms.FileField(required= True, label= u"Upload the Excel file to import to the system.")

    def clean_input_excel(self):
        input_excel = self.cleaned_data['input_excel']
        extension = os.path.splitext( input_excel.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s is not a valid excel file. Please make sure your input file is an excel file (Excel 2007 is NOT supported.' % extension )
        else:
            return input_excel

    class Meta:
        model = Work
        widgets = {'initialDate': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}),
                   'finalDate': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}),
                   'affectTime': DateTimePicker(options={"format": "HH:mm",
                                       "pickSeconds": False, "pickDate": False}),
                   'rollbackTime': DateTimePicker(options={"format": "HH:mm",
                                       "pickSeconds": False, "pickDate": False})}
        exclude = ['description', 'justification', 'observations', 'number']


class AcceptanceForm(forms.ModelForm):
    class Meta:
        model = Acceptance
        exclude = ['work', 'valid', 'token', 'notifiedDate', 'responseDate', 'nit']
