from django.urls import path
from . import views

#URL configerations
urlpatterns = [
    path('',views.home, name='home'),
    path('property_valuation/', views.property_view, name='property_view'),
    path('get-cities/<int:district_id>/', views.get_cities, name='get_cities'),
    path('about/', views.about, name ="about"),
    path('valuation/', views.valuation, name ="valuation"),
    path('result/', views.result, name='result'),
    #path('models/', views.models, name = "models"),
    
]