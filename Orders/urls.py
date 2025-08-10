from django.urls import path
from .views import *

urlpatterns = [
    path('customers/', CustomerList.as_view()),
    path('products/', ProductList.as_view()),
]