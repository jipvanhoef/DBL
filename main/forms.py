import os
from django.contrib import messages
from django import forms

from data_visualization.models import Data_set
class Data_setForm(forms.ModelForm):
    class Meta:
        model = Data_set
        fields = [
            'file'
        ]

    #overide the clean function for the data in the form
    def clean(self):
        #declare the list of supported file types
        supported_file_types = ['.csv']
        #clean the data from the form by calling the parent method
        cleaned_data = super(Data_setForm,self).clean()
        #get the file from the form
        file = cleaned_data.get('file')
        
        #check if the file is correctly loaded
        if not file == None:
            #get the filetype by splitting of the extension from the name
            filetype = os.path.splitext(file.name)[1]
            #check if the filetype is in the list of supported files
            if not filetype in supported_file_types:
                #raise a forms validation error with our error message
                raise forms.ValidationError("Wrong file type")

