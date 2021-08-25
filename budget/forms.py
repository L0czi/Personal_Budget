from django import forms
from . models import Expence, Income, ExpenceCategory, ExpenceWay, IncomeCategory
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class IncomeCategoryForm (forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']
        labels ={
            'name':(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nowa Kategoria', 'id':'input-category'}),
        }
    
    def clean_name(self):
        data = self.cleaned_data['name'].title()
        if len(data) > 15:
            data = data[0:15]
        return data 

class ExpenceCategoryForm (forms.ModelForm):
    class Meta:
        model = ExpenceCategory
        fields = ['name']
        labels ={
            'name':(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nowa Kategoria'}),
        }

class WayCategoryForm (forms.ModelForm):
    class Meta:
        model = ExpenceWay
        fields = ['name']
        labels ={
            'name':(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nowa Kategoria'}),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class AddExpenceForm (forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['ammount','expence_way','expence_category','date', 'notes']

        labels = {
            'ammount':'Kwota:',
            'expence_category': 'Kategoria:',
            'expence_way': 'Płatność:',
            'date':'Data:',
            'notes':'Notatki:',
        }
        widgets = {
            'expence_category':forms.RadioSelect(),
            'expence_way':forms.RadioSelect(),
            'notes': forms.TextInput(attrs={'placeholder': 'Opcjonalnie...'}),
            'date': forms.DateInput()
        }
    
    def __init__(self,user, *args, **kwargs):
        super(AddExpenceForm, self).__init__(*args,**kwargs)
        self.fields ['expence_category'].queryset = ExpenceCategory.objects.filter(user=user)
        self.fields ['expence_way'].queryset = ExpenceWay.objects.filter(user=user)
    
    def clean_ammount(self):
        data = self.cleaned_data['ammount']

        #check if given ammount is greater than 0
        if data <= 0:
            raise ValidationError(_("Podana kwota musi być większa od zera"), code='invalid')

        return data

class AddIncomeForm (forms.ModelForm):
    class Meta:
        model = Income
        fields = ['ammount','income_category','date','notes']
        
        labels = {
            'ammount':'Kwota:',
            'income_category': 'Kategoria:',
            'date':'Data:',
            'notes':'Notatki:',
        }
        widgets = {
            'income_category':forms.RadioSelect(),
            'notes': forms.TextInput(attrs={'placeholder': 'Opcjonalnie...'}),
            'date': forms.DateInput()
        }
    
    def __init__(self,user, *args, **kwargs):
        super(AddIncomeForm, self).__init__(*args,**kwargs)
        self.fields ['income_category'].queryset = IncomeCategory.objects.filter(user=user)
    
    def clean_ammount(self):
        data = self.cleaned_data['ammount']

        #check if given ammount is greater than 0
        if data <= 0:
            raise ValidationError(_("Podana kwota musi być większa od zera"), code='invalid')

        return data
        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-field','placeholder': 'email'}),)

    password1 = forms.CharField( 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'input-field','placeholder': 'Hasło'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'input-field','placeholder': 'Potwórz hasło'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username' :forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Użytkownik'}),
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-field', 
            'placeholder': 'Użytkownik', 
}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input-field',
            'placeholder': 'Hasło',
}))