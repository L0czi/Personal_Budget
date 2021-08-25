from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    #path('ajax/add_income_category', views.add_income_category, name='ajax-income-ctegory'),

    path('e_exp_category/<str:name>',views.expence_category_update, name='settings-exp-cat-update'),
    path('e_inc_category/<str:name>',views.income_category_update, name='settings-inc-cat-update'),
    path('e_way_category/<str:name>',views.way_category_update, name='settings-way-cat-update'),

    path('expence/', views.create_expence, name = 'create-expence'),
    path('income/', views.create_income, name='create-income'),
    path('balance/', views.balance, name = 'balance')
]