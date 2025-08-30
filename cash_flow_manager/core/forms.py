from django import forms
from .models import Transaction, Category, Subcategory, TransactionType, Status


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type_id=self.instance.type)
            
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=self.instance.category)
        
        
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount',  'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
            'status': forms.Select(attrs={'class': 'form-select'}), 
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'type-select'}), 
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'category-select'}), 
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'subcategory-select'}), 
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000', 'step': '0.01'}),  
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
        }
        
    def clean(self):
        cleaned = super().clean()
        ts_type = cleaned.get('type')
        category = cleaned.get('category')
        subcategory = cleaned.get('subcategory')

        if category and category.type != ts_type:
            self.add_error('category', 'Категория не относится к выбранному типу')

        if subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Подкатегория не относится к выбранной категории')

        return cleaned
    
    
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите статус'})
        }
        

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тип транзакции'})
        }
        

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = TransactionType.objects.all()
        
        
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите категорию транзакции'}),
            'type': forms.Select(attrs={'class': 'form-select'})
        }
        
    def clean_type(self):
        new_type = self.cleaned_data['type']
        
        if self.instance.pk:
            if self.instance.subcategories.exists() and new_type != self.instance.type:
                raise forms.ValidationError('Нельзя менять тип категории, если у неё есть подкатегории.')

        return new_type
        
        
class SubcategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        
        
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите подкатегорию транзакции'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }