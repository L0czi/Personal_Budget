from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    
    path('expence_category/<int:pk>/update',views.expence_category_update, name='expence-category-update'),
    path('income_category/<int:pk>/update',views.income_category_update, name='income-category-update'),
    path('expence_way/<int:pk>/update',views.way_category_update, name='expence-way-category-update'),

     path('expence_category/<int:pk>/delete', views.ExpenceCategoryDeleteView.as_view(), name='expence-category-delete'),
     path('income_category/<int:pk>/delete', views.IncomeCategoryDeleteView.as_view(), name='income-category-delete'),
     path('expence_way/<int:pk>/delete', views.ExpenceWayCategoryDeleteView.as_view(), name='expence-way-category-delete'),

    path('expence/', views.create_expence, name = 'create-expence'),
    path('income/', views.create_income, name='create-income'),
    path('balance/', views.balance, name = 'balance')
]