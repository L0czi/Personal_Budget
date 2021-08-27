from django.shortcuts import render, redirect
from . models import ExpenceCategory, ExpenceWay, IncomeCategory, Expence, Income
from . forms import AddExpenceForm, UserRegisterForm, ExpenceCategoryForm,  WayCategoryForm, IncomeCategoryForm, AddIncomeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class IncomeCategoryDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = IncomeCategory
    success_url = reverse_lazy('settings')


@login_required
def index(request):

    return render (request, 'budget/index.html')

@login_required
def balance(request):
    '''User Expence data'''
    # Querry all expence categorys assigned to currently log user
    all_expences_categorys = ExpenceCategory.objects.filter(user=request.user)
    # Create a lits of all categorys id 
    all_expences_categorys_id = [all_expences_categorys[i].id for i in range(0,len(all_expences_categorys))]
    # Querry all user expence wich match user expence category id sorted by last added
    all_expences = Expence.objects.filter(expence_category__in=all_expences_categorys_id).order_by('-date', '-id')

    # All expences aggragate by category for currently log user
    aggr_exp_query = [Expence.objects
        .filter( 
            expence_category=expence_category)
        .aggregate(Sum('ammount'))['ammount__sum'] for expence_category in all_expences_categorys_id]
    
    # Create a tuple - (expence category name, summary expence for category)
    aggr_expences = list(zip(all_expences_categorys, aggr_exp_query))

    '''User Income data'''
    # Querry all income categorys assigned to currently log user
    all_incomes_categorys = IncomeCategory.objects.filter(user=request.user)
    # Create a lits of all categorys id 
    all_incomes_categorys_id = [all_incomes_categorys[i].id for i in range(0,len(all_incomes_categorys))]
    # Querry all user expence wich match user expence category id sorted by last added
    all_incomes = Income.objects.filter(income_category__in=all_incomes_categorys_id).order_by('-date', '-id')

    #All incomes aggragate by category for currently log user
    aggr_incomes_query = [Income.objects
        .filter(
            income_category=income_category)
        .aggregate(Sum('ammount'))['ammount__sum'] for income_category in all_incomes_categorys_id]

    aggr_incomes = list(zip(all_incomes_categorys, aggr_incomes_query))

    '''Balance'''
    #Sum all expences
    aggr_all_expences = all_expences.aggregate(Sum('ammount'))['ammount__sum']
    #Sum all incomes
    aggr_all_incomes = all_incomes.aggregate(Sum('ammount'))['ammount__sum']
    #Balance
    if aggr_all_incomes == None:
        aggr_all_incomes = 0
    
    if aggr_all_expences == None:
        aggr_all_expences = 0
        
    balance = aggr_all_incomes - aggr_all_expences

    context = {
        'aggr_expences': aggr_expences,
        'aggr_all_expences':aggr_all_expences,
        'all_expences': all_expences,
        'aggr_incomes': aggr_incomes,
        'aggr_all_incomes':aggr_all_incomes,
        'all_incomes': all_incomes,
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
    income_category = IncomeCategory.objects.filter(user=request.user)
    form = IncomeCategoryForm(request.POST or None)
    data = {}
    
    if request.method == 'POST':
        if form.is_valid():
            category = form.save(commit=False)

            if IncomeCategory.objects.filter(user=request.user, name=category.name):
                data['errorText'] = f'Błąd! Kategoria "{category.name}" już istnieje!!'
                return JsonResponse(data, status=400)

            else:
                new_category = IncomeCategory.objects.create(user=request.user, name=category.name)
                new_category.save()
                data['name'] = form.cleaned_data.get('name')
                data['id'] = new_category.id
                data['status'] = 'ok'
                return JsonResponse(data)

    context = {
    #'form_add_ex_cat':form_add_ex_cat,
    'form_add_in_cat':form,
    #'form_add_way':form_add_way,
    #'expence_cat':expence_cat,
    #'expence_way':expence_way,
    'income_cat':income_category,
    }
    
    return render(request, 'budget/settings.html', context)



'''
@login_required
def add_income_category(request):
    if request.method == 'POST':

        form = IncomeCategoryForm(request.POST)

        if form.is_valid():
            category = form.save()
            cat_ser = serializers.serialize('jason', [category])
            return JsonResponse({'category':cat_ser}, status=200)
            
            
            #check if user already have a category with given name
            if IncomeCategory.objects.filter(user=request.user, name=category.name[0:15].title()):
                messages.warning(request, f'Błąd! Kategoria "{category.title()}" już istnieje!!')
            else:
                new_category = IncomeCategory.objects.create(user=request.user, name=category.name[0:15].title())
                new_category.save()
                return redirect('settings')
            
        else:
            # some form errors occured.
            return JsonResponse({"error": "a"}, status=400)

    return JsonResponse({"error": "b"}, status=400)

@login_required
def settings (request):

    #expence_cat = ExpenceCategory.objects.filter(user = request.user)
    #form_add_ex_cat = ExpenceCategoryForm()
    
    income_cat = IncomeCategory.objects.filter(user = request.user)
    form_add_in_cat = IncomeCategoryForm()

    #expence_way = ExpenceWay.objects.filter(user = request.user)
    #form_add_way = WayCategoryForm()

    context = {
    #'form_add_ex_cat':form_add_ex_cat,
    'form_add_in_cat':form_add_in_cat,
    #'form_add_way':form_add_way,
    #'expence_cat':expence_cat,
    #'expence_way':expence_way,
    'income_cat':income_cat,
    }
    return render(request, 'budget/settings.html', context)

    
    if request.method == 'POST': #and "add_expence_category" in request.POST:
        form = IncomeCategoryForm(request.POST)

        if form.is_valid():
            add_category(form=form, model=IncomeCategory, request=request)
            return redirect('settings')

        
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
'''
@login_required
def expence_category_update (request, name):
    if request.method == 'POST':
        form = ExpenceCategoryForm(request.POST, instance=ExpenceCategory.objects.filter(user=request.user, name=name).first())
        if form.is_valid():
            category = form.save(commit=False)

            if ExpenceCategory.objects.filter(user=request.user, name=category.name.title()):
                messages.warning(request, f'Błąd! Kategoria "{category.name.title()}" już istnieje!!')
            else:
                category.name = category.name[0:15]
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
                category.name = category.name[0:15]
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
                category.name = category.name[0:15]
                category.save()
            return redirect('settings')
    else:
       form = WayCategoryForm(instance=ExpenceWay.objects.filter(user=request.user, name=name).first())

    context = {
        'form': form,
    }
    
    return render(request,'budget/category_update.html',context)

def register(request):
    
    if request.user.is_authenticated:
        return redirect('index')

    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            default_expence_cat = ['Transport',
            'Jedzenie', 'Książki', 'Mieszkanie','Telekomunikacja',
            'Zdrowie', 'Odzież', 'Higiena', 'Dzieci', 'Rekreacja',
            'Wycieczki', 'Oszczędności', 'Prezenty', 'Inne'
            ]

            for category in default_expence_cat:
                ExpenceCategory.objects.create(user=user,name=category)
            
            default_expence_way = ['Gotówka', 'Karta kredytowa', 'Karta płatnicza']
            for category in default_expence_way:
                ExpenceWay.objects.create(user=user,name=category)
            
            default_income_cat = ['Pensja', 'Odsetki', 'Inne']
            for category in default_income_cat:
                IncomeCategory.objects.create(user=user,name=category)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto zostało założone {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'budget/register.html', {'form': form})
