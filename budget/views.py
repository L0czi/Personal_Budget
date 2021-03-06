from django.shortcuts import render, redirect
from . models import ExpenceCategory, ExpenceWay, IncomeCategory, Expence, Income
from . forms import AddExpenceForm, UserRegisterForm, ExpenceCategoryForm,  WayCategoryForm, IncomeCategoryForm, AddIncomeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.core import serializers


class IncomeCategoryDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = IncomeCategory
    success_url = reverse_lazy('settings')

class ExpenceCategoryDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = ExpenceCategory
    success_url = reverse_lazy('settings')

class ExpenceWayCategoryDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = ExpenceWay
    success_url = reverse_lazy('settings')

class IncomeDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Income
    success_url = reverse_lazy('balance')

class ExpenceDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Expence
    success_url = reverse_lazy('balance')

@login_required
def chart_data(request):

    data = {}

    user_expences_categories = ExpenceCategory.objects.filter(user=request.user)

    user_expences_categories_name = [user_expences_categories[i].name for i in range (0, len(user_expences_categories))]
    user_expences_categories_id = [user_expences_categories[i].id for i in range(0,len(user_expences_categories))]
    
    user_expences_aggregate_query = [Expence.objects
    .filter( 
        expence_category=expence_category)
    .aggregate(Sum('ammount'))['ammount__sum'] for expence_category in user_expences_categories_id]

    user_expences_ammount = [user_expences_aggregate_query[i] if user_expences_aggregate_query[i] !=None else 0 for i in range (0, len(user_expences_aggregate_query))]

    result = list(zip(user_expences_categories_name, user_expences_ammount))

    chart_data = [{'label':label,'ammount':int(ammount)} for (label, ammount) in result]

    data['chart_data'] = chart_data
    
    return JsonResponse(data, status=200)    

@login_required
def index(request):

    return render (request, 'budget/index.html')

def aggregate_all(aggr):
    aggregated = aggr.aggregate(Sum('ammount'))['ammount__sum']
    
    if aggregated == None:
        return 0
    else:
        return aggregated

@login_required
def balance(request):
    data = {}
    '''User Expence data'''
    # Querry all expence categorys assigned to currently log user
    user_expences_categories = ExpenceCategory.objects.filter(user=request.user)
    # Create a lits of all categorys id 
    user_expences_categories_id = [user_expences_categories[i].id for i in range(0,len(user_expences_categories))]
    # Querry all user expences wich match user expence category id sorted by last added
    all_user_expences = Expence.objects.filter(expence_category__in=user_expences_categories_id).order_by('-date', '-id')
    
    # All expences aggragate by category for currently log user
    user_expences_aggregate_query = [Expence.objects
        .filter( 
            expence_category=expence_category)
        .aggregate(Sum('ammount'))['ammount__sum'] for expence_category in user_expences_categories_id]
    
    # Create a tuple - (expence category name, summary expence for category)
    user_expences_aggregate = list(zip(user_expences_categories, user_expences_categories_id ,user_expences_aggregate_query))

    '''User Income data'''
    # Querry all income categorys assigned to currently log user
    user_incomes_categories = IncomeCategory.objects.filter(user=request.user)
    # Create a lits of all categorys id 
    user_incomes_categories_id = [user_incomes_categories[i].id for i in range(0,len(user_incomes_categories))]
    # Querry all user expence wich match user expence category id sorted by last added
    all_user_incomes = Income.objects.filter(income_category__in=user_incomes_categories_id).order_by('-date', '-id')
    #All incomes aggragate by category for currently log user
    user_incomes_aggregate_query = [Income.objects
        .filter(
            income_category=income_category)
        .aggregate(Sum('ammount'))['ammount__sum'] for income_category in user_incomes_categories_id]

    user_incomes_aggregate = list(zip(user_incomes_categories, user_incomes_categories_id, user_incomes_aggregate_query))

    '''Balance'''
    #Sum all expences
    aggr_all_user_expences = aggregate_all(aggr=all_user_expences)
    #Sum all incomes
    aggr_all_user_incomes = aggregate_all(aggr=all_user_incomes)
    #Balance        
    balance = aggr_all_user_incomes - aggr_all_user_expences

    if request.method == 'GET' and 'AJAX' in request.GET:

        updated_aggr_all_expences = aggregate_all(aggr=all_user_expences)
        updated_all_incomes = aggregate_all(aggr=all_user_incomes)
        updated_balance = updated_all_incomes - updated_aggr_all_expences

        if request.GET['type'] == 'expence':
            updated_category_value = Expence.objects.filter( expence_category=request.GET['category']).aggregate(Sum('ammount'))['ammount__sum']

        elif request.GET['type'] =='income':
            updated_category_value = Income.objects.filter( income_category=request.GET['category']).aggregate(Sum('ammount'))['ammount__sum']
        ####################################################################################
        data['aggr_all_expences'] = updated_aggr_all_expences
        data['aggr_all_incomes'] = updated_all_incomes
        data['balance'] = updated_balance
        data['updated_category_value'] = updated_category_value

        return JsonResponse(data, status=200)

    context = {
        'aggr_expences': user_expences_aggregate,
        'aggr_all_expences':aggr_all_user_expences,
        'all_expences': all_user_expences,

        'aggr_incomes': user_incomes_aggregate,
        'aggr_all_incomes':aggr_all_user_incomes,
        'all_incomes': all_user_incomes,

        'balance':balance,
    }

    return render(request,'budget/balance.html', context)

@login_required
def create_income(request):
    if request.method == 'POST':
        form = AddIncomeForm(request.user, request.POST)
        if form.is_valid():
            income = form.save(commit=False)

            if income.notes.isspace() or len(income.notes)==0:
                income.notes = 'Nie dodano notatki'

            add_income = Income.objects.create(

            user=request.user,  
            income_category=income.income_category,
            ammount = income.ammount,
            date = income.date,
            notes = income.notes
            )
            
            add_income.save()
            messages.success(request, f'Dodano przych??d')
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

            if expence.notes.isspace() or len(expence.notes)==0:
                expence.notes = 'Nie dodano notatki'

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
def settings(request):
    incomes_categories = IncomeCategory.objects.filter(user=request.user)
    income_category_form = IncomeCategoryForm(request.POST or None)

    expences_categories = ExpenceCategory.objects.filter(user=request.user)
    expence_category_form = ExpenceCategoryForm(request.POST or None)

    expences_ways = ExpenceWay.objects.filter(user=request.user)
    expence_way_form = WayCategoryForm(request.POST or None)

    data = {}
    
    if request.method == 'POST' and 'addIncomeCategoryButton' in request.POST:
        if income_category_form.is_valid():
            category = income_category_form.save(commit=False)

            if IncomeCategory.objects.filter(user=request.user, name=category.name):
                data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
                return JsonResponse(data, status=400)

            else:
                new_category = IncomeCategory.objects.create(user=request.user, name=category.name)
                new_category.save()
                data['name'] = income_category_form.cleaned_data.get('name')
                data['id'] = new_category.id
                data['succesText'] = f'Dodano now?? kategori?? - "{new_category.name}"'
                return JsonResponse(data, status=200)

    elif request.method == 'POST' and 'addExpenceCategoryButton' in request.POST:
        if expence_category_form.is_valid():
            category = expence_category_form.save(commit=False)

            if ExpenceCategory.objects.filter(user=request.user, name=category.name):
                data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
                return JsonResponse(data, status=400)

            else:
                new_category = ExpenceCategory.objects.create(user=request.user, name=category.name)
                new_category.save()
                data['name'] = expence_category_form.cleaned_data.get('name')
                data['id'] = new_category.id
                data['succesText'] = f'Dodano now?? kategori?? - "{new_category.name}"'
                return JsonResponse(data, status=200)
    
    elif request.method == 'POST' and 'addExpenceWayButton' in request.POST:
        if expence_way_form.is_valid():
            category = expence_way_form.save(commit=False)

            if ExpenceWay.objects.filter(user=request.user, name=category.name):
                data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
                return JsonResponse(data, status=400)

            else:
                new_category = ExpenceWay.objects.create(user=request.user, name=category.name)
                new_category.save()
                data['name'] = expence_way_form.cleaned_data.get('name')
                data['id'] = new_category.id
                data['succesText'] = f'Dodano now?? kategori?? - "{new_category.name}"'
                return JsonResponse(data, status=200)

    context = {
    'income_category_form':income_category_form,
    'expence_category_form':expence_category_form,
    'expence_way_form':expence_way_form,
    'incomes_categories':incomes_categories,
    'expences_categories':expences_categories,
    'expences_ways':expences_ways,
    }
    
    return render(request, 'budget/settings.html', context)

@login_required
def income_category_update (request, pk):

    form = IncomeCategoryForm(request.POST or None, instance=IncomeCategory.objects.filter(user=request.user, id=pk).first())
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            category = form.save(commit=False)

            if IncomeCategory.objects.filter(user=request.user, name=category.name):
                data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
                return JsonResponse(data, status=400)
            
            else:
                category.save()
                data['name'] = form.cleaned_data.get('name')
                return JsonResponse(data, status=200)
    else:
        category = IncomeCategory.objects.filter(user=request.user, id=pk).first()
        data['name'] = category.name
        return JsonResponse(data, status=200)

@login_required
def expence_category_update (request, pk):

    form = ExpenceCategoryForm(request.POST or None, instance=ExpenceCategory.objects.filter(user=request.user, id=pk).first())
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            category = form.save(commit=False)

            if ExpenceCategory.objects.filter(user=request.user, name=category.name):
               data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
               return JsonResponse(data, status=400)

            else:
                category.save()
                data['name'] = form.cleaned_data.get('name')
                return JsonResponse(data, status=200)
    else:
        category = ExpenceCategory.objects.filter(user=request.user, id=pk).first()
        data['name'] = category.name
        return JsonResponse(data, status=200)

@login_required
def way_category_update (request, pk):

    form = WayCategoryForm(request.POST or None, instance=ExpenceWay.objects.filter(user=request.user, id=pk).first())
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            category = form.save(commit=False)

            if ExpenceWay.objects.filter(user=request.user, name=category.name):
               data['errorText'] = f'B????d! Kategoria "{category.name}" ju?? istnieje!!'
               return JsonResponse(data, status=400)
            
            else:
                category.save()
                data['name'] = form.cleaned_data.get('name')
                return JsonResponse(data, status=200)
    else:
        category = ExpenceWay.objects.filter(user=request.user, id=pk).first()
        data['name'] = category.name
        return JsonResponse(data, status=200)

def register(request):
    
    if request.user.is_authenticated:
        return redirect('index')

    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            default_expence_cat = ['Transport',
            'Jedzenie', 'Ksi????ki', 'Mieszkanie','Telekomunikacja',
            'Zdrowie', 'Odzie??', 'Higiena', 'Dzieci', 'Rekreacja',
            'Wycieczki', 'Oszcz??dno??ci', 'Prezenty', 'Inne'
            ]

            for category in default_expence_cat:
                ExpenceCategory.objects.create(user=user,name=category)
            
            default_expence_way = ['Got??wka', 'Karta kredytowa', 'Karta p??atnicza']
            for category in default_expence_way:
                ExpenceWay.objects.create(user=user,name=category)
            
            default_income_cat = ['Pensja', 'Odsetki', 'Inne']
            for category in default_income_cat:
                IncomeCategory.objects.create(user=user,name=category)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zosta??o za??o??one {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'budget/register.html', {'form': form})
