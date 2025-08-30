from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction

admin.site.register(Status)
admin.site.register(TransactionType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Transaction)