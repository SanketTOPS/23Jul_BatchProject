from django import forms
from .models import userSignup,notes

class signupForm(forms.ModelForm):
    class Meta:
        model=userSignup
        fields='__all__'
    
class UpdateForm(forms.ModelForm):
    class Meta:
        model=userSignup
        fields=['username'] #optional

class notesForm(forms.ModelForm):
    class Meta:
        model=notes
        fields='__all__'