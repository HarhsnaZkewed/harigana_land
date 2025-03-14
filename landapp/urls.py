from django.urls import path
from . import views

#URL configerations
urlpatterns = [

    #URL directs for normal pages
    path('',views.home, name='home'),
    path('about/', views.about, name ="about"),
    path('valuation_home/', views.valuation_home, name="valuation_home"),

    #URL directs for the property valuations
    path('property_valuation/', views.property_view, name='property_valuation'),
    path('get-cities/<int:district_id>/', views.get_cities, name='get_cities'),
   
    #URL directs for the vehicle valuations
    path('vehicle_valuation/', views.vehicle_valuation, name ="vehicle_valuation"),
    path('get-models/<int:make_id>/', views.get_models, name='get_models'),
    path('vehicle-closest/', views.closest, name='vehicle-closest'),
    
    path('submit-vehicle-feedback/', views.submit_vehicle_feedback, name='submit_vehicle_feedback'),
    path('submit-land-feedback/', views.submit_land_feedback, name='submit_land_feedback'),
    
]