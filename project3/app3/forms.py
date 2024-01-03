from django import forms
from .models import medical

class medicalForm(forms.ModelForm):
    class Meta:
        model = medical
        fields = ['name','quantity','price','expirydate']
