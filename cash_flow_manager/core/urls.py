from django.urls import path
from . import views


urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('add', views.TransactionCreateView.as_view(), name='transaction_add'),
    path('edit/<int:pk>', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('delete/<int:pk>', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    
    path('statuses/', views.StatusListView.as_view(), name='status_list'),
    path('statuses/add', views.StatusCreateView.as_view(), name='status_add'),
    path('statuses/edit/<int:pk>', views.StatusUpdateView.as_view(), name='status_edit'),
    path('statuses/delete/<int:pk>', views.StatusDeleteView.as_view(), name='status_delete'),
    
    path('types/', views.TypeListView.as_view(), name='type_list'),
    path('types/add', views.TypeCreateView.as_view(), name='type_add'),
    path('types/edit/<int:pk>', views.TypeUpdateView.as_view(), name='type_edit'),
    path('types/delete/<int:pk>', views.TypeDeleteView.as_view(), name='type_delete'),
    
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/add', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/edit/<int:pk>', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    path('subcategory/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategory/add', views.SubcategoryCreateView.as_view(), name='subcategory_add'),
    path('subcategory/edit/<int:pk>', views.SubcategoryUpdateView.as_view(), name='subcategory_edit'),
    path('subcategory/delete/<int:pk>', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
    
    path('ajax/load-categories/', views.ajax_load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.ajax_load_subcategories, name='ajax_load_subcategories'),
]
