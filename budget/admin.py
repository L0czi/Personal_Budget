from django.contrib import admin
from . models import ExpenceWay, Expence, ExpenceCategory, Income, IncomeCategory

admin.site.register(ExpenceWay)
admin.site.register(Expence)
admin.site.register(ExpenceCategory)
admin.site.register(IncomeCategory)
admin.site.register(Income)
