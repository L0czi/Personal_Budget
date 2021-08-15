from django.contrib import admin
from . models import ExpenceWay, Expence, ExpenceCategory, Income, IncomeCategory

#admin.site.register(ExpenceWay)
#admin.site.register(Expence)
#admin.site.register(ExpenceCategory)
#admin.site.register(IncomeCategory)
#admin.site.register(Income)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user','income_category','ammount','date','notes')
    list_filter = ('user', 'date')

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('user',)

@admin.register(Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ('user','expence_category','expence_way','ammount','date','notes')
    list_filter = ('user', 'date')

@admin.register(ExpenceCategory)
class ExpenceCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('user',)

@admin.register(ExpenceWay)
class ExpenceWayAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('user',)