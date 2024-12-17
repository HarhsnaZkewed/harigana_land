from django.urls import path
from . import views

#URL configerations
urlpatterns = [

    #URL directs for normal pages
    path('',views.home, name='home'),
    path('about/', views.about, name ="about"),

    #URL directs for the property valuations
    path('property_valuation/', views.property_view, name='property_view'),
    path('get-cities/<int:district_id>/', views.get_cities, name='get_cities'),
   
    #URL directs for the vehicle valuations
    path('vehicle_valuation/', views.vehicle_valuation, name ="vehicle_valuation"),
    path('get-models/<int:make_id>/', views.get_models, name='get_models'),
    path('vehicle-closest/', views.closest, name='vehicle-closest'),
    

    
]