from django import forms
from django.forms import widgets
from django.forms.widgets import RadioSelect
from . models import Expence, Income, ExpenceCategory, ExpenceWay, IncomeCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IncomeCategoryForm (forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']
        labels ={
            'name':(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nowa Kategoria'}),
        }

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

class AddExpenceForm (forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['ammount','expence_way','expence_category','date']
        widgets = {
            'expence_category': RadioSelect,
            'expence_way': RadioSelect,
        }
    
    def __init__(self,user, *args, **kwargs):
        super(AddExpenceForm, self).__init__(*args,**kwargs)
        self.fields ['expence_category'].queryset = ExpenceCategory.objects.filter(user=user)
        self.fields ['expence_way'].queryset = ExpenceWay.objects.filter(user=user)

class DateInput(forms.DateInput):
    input_type = 'date'


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

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']