import os
from django.contrib import messages
from django import forms

from .models import Data_set

class Data_setForm(forms.ModelForm):
    class Meta:
        model = Data_set
        fields = [
            'file'
        ]
    
    def clean(self):
        supported_file_types = ['.csv']
        cleaned_data = super(Data_setForm,self).clean()
        file = cleaned_data.get('file')
         
        if file:
            filetype = os.path.splitext(file.name)[1]
            error_string = "The file type " + filetype + " is at this moment not suported please summit a "
            for i in range(len(supported_file_types)):
                if i == len(supported_file_types) - 1:
                    error_string = error_string + supported_file_types[i]
                else:
                    error_string = error_string + supported_file_types[i] + ", "

            error_string = error_string + " file."
            if not filetype in supported_file_types:
                raise forms.ValidationError(error_string)

