from django.urls import path
from . import views


app_name = 'cupon'
urlpatterns = [
    path('apply', views.cupon_apply, name='apply')
]
