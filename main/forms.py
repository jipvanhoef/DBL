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
            #Create the error message
            error_string = "The file type " + filetype + " is not suported please summit a "
            
            #add all the supported file types to the error message
            for i in range(len(supported_file_types)):
                #if it is the last entry do not ad a comma
                if i == len(supported_file_types) - 1:
                    #add the file type to the error string
                    error_string = error_string + supported_file_types[i]
                else:
                    #add the file type followed by a comma to the error string
                    error_string = error_string + supported_file_types[i] + ", "

            #complete the error string
            error_string = error_string + " file."
            #check if the filetype is in the list of supported files
            if not filetype in supported_file_types:
                #raise a forms validation error with our error message
                raise forms.ValidationError("Wrong file type")

