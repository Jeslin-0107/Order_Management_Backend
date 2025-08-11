from django.urls import path
from .views import *

urlpatterns = [
    path('customers/', CustomerList.as_view()),
    path('products/', ProductList.as_view()),
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('orders/<int:pk>/status/', OrderUpdateStatusView.as_view()),

]