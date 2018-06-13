from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('<category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug>/', views.product_detail, name='product_detail'),
    path('', views.product_list, name='product_list')
]
