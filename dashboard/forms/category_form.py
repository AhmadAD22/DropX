from django import forms
from restaurant.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        labels = {
            'name': 'اسم التصنيف',
            'image': 'رفع الصورة',
        }
        labels = {
            'image': 'حمل صورة',
            'name': 'إسم التصنيف',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }