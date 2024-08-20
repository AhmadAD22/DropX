from django import forms
from ..models import CommonQuestion

class CommonQuestionForm(forms.ModelForm):
    class Meta:
        model = CommonQuestion
        fields = ['question', 'answer']
        widgets = {

            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Answer'}),
        }