from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.contrib import messages

from .models import Transaction, TransactionType, Status, Category, Subcategory
from .forms import TransactionForm, TransactionTypeForm, StatusForm, CategoryForm, SubcategoryForm


#
# Transaction Views
#

class TransactionListView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by('-date')
        return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


class TransactionCreateView(View):
    def get(self, request):
        form = TransactionForm()
        return  render(request, 'transactions/transaction_form.html', {'form': form})
    
    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
        return render(request, 'transactions/transaction_form.html', {'form': form})
    
    
class TransactionUpdateView(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        form = TransactionForm(instance=transaction)
        return render(request, 'transactions/transaction_form.html', {'form': form})
    
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
        
        return render(request, 'transactions/transaction_form.html', {'form': form})
    

class TransactionDeleteView(View):
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return redirect('transaction_list')
    
    
#
# Status Views
#

class StatusListView(ListView):
    model = Status
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('status_list')


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('status_list')


class StatusDeleteView(View):
    def post(self, request, pk):
        try:
            status = get_object_or_404(Status, pk=pk)
            status.delete()
        except ProtectedError:
            messages.error(request, 'Нельзя удалить объект. Есть связанные транзакции')
        return redirect('status_list')
    
    
#
# Types Views
#

class TypeListView(ListView):
    model = TransactionType
    template_name = 'transaction_type/type_list.html'
    context_object_name = 'types'


class TypeCreateView(CreateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'transaction_type/type_form.html'
    success_url = reverse_lazy('type_list')


class TypeUpdateView(UpdateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'transaction_type/type_form.html'
    success_url = reverse_lazy('type_list')


class TypeDeleteView(View):
    def post(self, request, pk):
        try:
            ts_type = get_object_or_404(TransactionType, pk=pk)
            ts_type.delete()
        except ProtectedError:
            messages.error(request, 'Нельзя удалить объект. Есть связанные транзакции')
        return redirect('type_list')
    
    
#
# Category Views
#

class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(View):
    def post(self, request, pk):
        try:
            category = get_object_or_404(Category, pk=pk)
            category.delete()
        except ProtectedError:
            messages.error(request, 'Нельзя удалить объект. Есть связанные транзакции')
        return redirect('category_list')
    
    
#
# Subcategory Views
#

class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'subcategory/subcategory_list.html'
    context_object_name = 'subcategories'


class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'subcategory/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'subcategory/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')


class SubcategoryDeleteView(View):
    def post(self, request, pk):
        try:
            subcategory = get_object_or_404(Subcategory, pk=pk)
            subcategory.delete()
        except ProtectedError:
            messages.error(request, 'Нельзя удалить объект. Есть связанные транзакции')
        return redirect('subcategory_list')


#
# Ajax loads
#

def ajax_load_categories(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def ajax_load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)