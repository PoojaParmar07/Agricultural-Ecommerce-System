from django.urls import path,include
from .views import home, category_list, category_add, category_view_detail

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
    path('category_list/',category_list,name='category_list'),
    path('category_add/',category_add,name='category_add'),
    path('category_view_detail/<int:pk>/',category_view_detail,name='category_view_detail'),
]





