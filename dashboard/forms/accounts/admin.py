from django import forms
from django.contrib.auth.models import Permission
from accounts.models import User

class UserCreationWithPermissionsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(content_type__model='user'), required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    fullName=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['phone', 'phone', 'fullName','password', 'nationality', 'is_superuser', 'permissions']

    def save(self, commit=True):
        user = super(UserCreationWithPermissionsForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.nationality = self.cleaned_data['nationality']
        user.is_staff = True
        user.is_superuser = self.cleaned_data['is_superuser']
        user.set_password(self.cleaned_data['password'])  # Set the password to the user
        if commit:
            user.save()
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user
    
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nationality = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(content_type__model='user'),
                                                 required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    fullName=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['phone','fullName','email', 'phone', 'nationality', 'is_superuser', 'permissions']
        
 
    

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['permissions'].initial = self.instance.user_permissions.all()