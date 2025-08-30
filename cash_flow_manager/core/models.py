from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    
    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='categories')
    
    
    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    
    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.date} | {self.amount} ₽ | {self.type} / {self.category} / {self.subcategory}'