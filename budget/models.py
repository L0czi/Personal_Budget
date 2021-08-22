from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.utils.timezone import now

class ExpenceCategory (models.Model):
    '''Model representing all possible category for expence'''
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    def __str__ (self):
        return self.name  

class ExpenceWay (models.Model):
    '''Model representing all possible expence way'''
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    def __str__ (self):
        return self.name 

class Expence (models.Model):
    '''Model representing particular expence'''
    expence_category = models.ForeignKey(ExpenceCategory, on_delete=CASCADE)
    expence_way = models.ForeignKey(ExpenceWay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    ammount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=now, blank=True)
    notes = models.CharField(max_length=100, blank=True)

    
    def __str__ (self):
        return f'{self.user}: {self.expence_category}, {self.expence_way}, {self.ammount}'  


class IncomeCategory (models.Model):
    '''Model representing all possible category for income'''
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    def __str__ (self):
        return self.name 

class Income (models.Model):
    '''Model representing particular income'''
    income_category = models.ForeignKey(IncomeCategory, on_delete=CASCADE, blank=False)
    user = models.ForeignKey(User, on_delete=CASCADE)
    ammount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=now, blank=True)
    notes = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__ (self):
        return f'{self.user}: {self.income_category}, {self.ammount}, {self.date}'  