from django import forms

from .models import Data_set

class Data_setForm(forms.ModelForm):
    class Meta:
        model = Data_set
        fields = [
            'data'
        ]