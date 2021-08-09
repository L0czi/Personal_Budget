from django.db.models.fields import CharField
from django.shortcuts import render, redirect, get_object_or_404
from . models import ExpenceCategory, ExpenceWay, IncomeCategory, Expence, Income
from . forms import AddExpenceForm, UserRegisterForm, ExpenceCategoryForm,  WayCategoryForm, IncomeCategoryForm, AddIncomeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum

@login_required
def balance(request):
    all_expences = Expence.objects.filter(user=request.user)
    all_incomes = Income.objects.filter(user=request.user)

    aggr_expences_query = Expence.objects.filter(user=request.user).aggregate(Sum('ammount'))
    aggr_expence = aggr_expences_query['ammount__sum']

    aggr_income_query = Income.objects.filter(user=request.user).aggregate(Sum('ammount'))
    aggr_income = aggr_income_query['ammount__sum']

    balance = aggr_income - aggr_expence

    context = {
        'balance':balance,
        'aggr_expence':aggr_expence,
        'aggr_income':aggr_income,
        'all_expences':all_expences,
        'all_incomes':all_incomes,
    }

    return render(request,'budget/balance.html', context)

@login_required
def create_income(request):
    if request.method == 'POST':
        form = AddIncomeForm(request.user, request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            add_income = Income.objects.create(

            user=request.user,  
            income_category=income.income_category,
            ammount = income.ammount,
            date = income.date,
            notes = income.notes
            )
            
            add_income.save()
            messages.success(request, f'Dodano przychód')
            return redirect('create-income')
    else:
       form = AddIncomeForm(user=request.user)

    context = {
        'form': form,
    }
    
    return render(request,'budget/income_form.html',context)


@login_required
def create_expence(request):
    if request.method == 'POST':
        form = AddExpenceForm(request.user, request.POST)
        if form.is_valid():
            expence = form.save(commit=False)
            add_expence = Expence.objects.create(
            
            user=request.user, 
            expence_way= expence.expence_way, 
            expence_category=expence.expence_category,
            ammount = expence.ammount,
            date = expence.date,
            notes = expence.notes
            )
            
            add_expence.save()
            messages.success(request, f'Dodano wydatek')
            return redirect('create-expence')
    else:
       form = AddExpenceForm(user=request.user)

    context = {
        'form': form,
    }
    
    return render(request,'budget/expence_form.html',context)

@login_required
def index(request):

    return render (request, 'budget/index.html')


def add_category(form, model, request):
    category = form.save(commit=False)
    #check if user already have a category with given name
    if model.objects.filter(user=request.user, name=category.name.title()):
        messages.warning(request, f'Błąd! Kategoria "{category.name.title()}" już istnieje!!')
    else:
        new_category = model.objects.create(user=request.user, name=category.name.title())
        new_category.save()

@login_required
def settings (request):

    if request.method == 'POST' and "add_expence_category" in request.POST:
        form_add_ex_cat = ExpenceCategoryForm(request.POST)

        if form_add_ex_cat.is_valid():
            add_category(form=form_add_ex_cat, model=ExpenceCategory, request=request)
            return redirect('settings')

    elif request.method == 'POST' and "add_income_category" in request.POST:
        form_add_in_cat = IncomeCategoryForm(request.POST)

        if form_add_in_cat.is_valid():
            add_category(form=form_add_in_cat, model=IncomeCategory, request=request)
            return redirect('settings')

    elif request.method == 'POST' and "add_expence_way" in request.POST:
        form_add_way = WayCategoryForm(request.POST)

        if form_add_way.is_valid():
            add_category(form=form_add_way, model=ExpenceWay, request=request)
            return redirect('settings')

    else:
        expence_cat = ExpenceCategory.objects.filter(user = request.user)
        form_add_ex_cat = ExpenceCategoryForm()

        income_cat = IncomeCategory.objects.filter(user = request.user)
        form_add_in_cat = IncomeCategoryForm()

        expence_way = ExpenceWay.objects.filter(user = request.user)
        form_add_way = WayCategoryForm()

    context = {
        'form_add_ex_cat':form_add_ex_cat,
        'form_add_in_cat':form_add_in_cat,
        'form_add_way':form_add_way,
        'expence_cat':expence_cat,
        'expence_way':expence_way,
        'income_cat':income_cat,
    }
    return render(request, 'budget/settings.html', context)

@login_required
def expence_category_update (request, name):
    if request.method == 'POST':
        form = ExpenceCategoryForm(request.POST, instance=ExpenceCategory.objects.filter(user=request.user, name=name).first())
        if form.is_valid():
            category = form.save(commit=False)

            if ExpenceCategory.objects.filter(user=request.user, name=category.name.title()):
                messages.warning(request, f'Błąd! Kategoria "{category.name.title()}" już istnieje!!')
            else:
                category.save()
            return redirect('settings')
    else:
       form = ExpenceCategoryForm(instance=ExpenceCategory.objects.filter(user=request.user, name=name).first())

    context = {
        'form': form,
    }
    
    return render(request,'budget/category_update.html',context)


@login_required
def income_category_update (request, name):
    if request.method == 'POST':
        form = IncomeCategoryForm(request.POST, instance=IncomeCategory.objects.filter(user=request.user, name=name).first())
        if form.is_valid():
            category = form.save(commit=False)

            if IncomeCategory.objects.filter(user=request.user, name=category.name.title()):
                messages.warning(request, f'Błąd! Kategoria "{category.name.title()}" już istnieje!!')
            else:
                category.save()
            return redirect('settings')
    else:
       form = IncomeCategoryForm(instance=IncomeCategory.objects.filter(user=request.user, name=name).first())

    context = {
        'form': form,
    }
    
    return render(request,'budget/category_update.html',context)

@login_required
def way_category_update (request, name):
    if request.method == 'POST':
        form = WayCategoryForm(request.POST, instance=ExpenceWay.objects.filter(user=request.user, name=name).first())
        if form.is_valid():
            category = form.save(commit=False)

            if ExpenceWay.objects.filter(user=request.user, name=category.name.title()):
                messages.warning(request, f'Błąd! Kategoria "{category.name.title()}" już istnieje!!')
            else:
                category.save()
            return redirect('settings')
    else:
       form = WayCategoryForm(instance=ExpenceWay.objects.filter(user=request.user, name=name).first())

    context = {
        'form': form,
    }
    
    return render(request,'budget/category_update.html',context)
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            default_espence_cat = ['Transport',
            'Jedzenie', 'Książki', 'Mieszkanie','Telekomunikacja',
            'Zdrowie', 'Odzież', 'Higiena', 'Dzieci', 'Rekreacja',
            'Wycieczki', 'Oszczędności', 'Prezenty', 'Inne'
            ]

            for category in default_espence_cat:
                ExpenceCategory.objects.create(user=user,name=category)
            
            default_expence_way = ['Gotówka', 'Karta kredytowa', 'Karta płatnicza']
            for category in default_expence_way:
                ExpenceWay.objects.create(user=user,name=category)
            
            default_income_category = ['Pensja', 'Odsetki', 'Inne']
            for category in default_income_category:
                IncomeCategory.objects.create(user=user,name=category)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zostało założone {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
        context = {
        'form': form,
    }
    return render(request, 'budget/register.html', context)
