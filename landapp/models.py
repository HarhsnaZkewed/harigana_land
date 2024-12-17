from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

#-------------------------------------------------------- Land Valuation --------------------------------------------------------------------

class PropertyDetails(models.Model):

    # Define fields of db  
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bedrooms = models.CharField(max_length=100)
    bathrooms = models.CharField(max_length=100)
    bathrooms = models.CharField(max_length=100)
    floor_area = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    property_details = models.CharField(max_length=100)
    property_features = models.CharField(max_length=100)
    property_type = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    perches = models.CharField(max_length=100)
    unit_price = models.CharField(max_length=100)


    class Meta:
        db_table = 'combined_tb'


class ProvinceDetails(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name_en = models.CharField(max_length=100)
    name_si = models.CharField(max_length=100, blank=True)
    name_ta = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'provinces'
         

    def __str__(self):
        return self.name_en


class DistrictDetails(models.Model):
    id = models.IntegerField(primary_key=True)  # Change to IntegerField
    province_id = models.ForeignKey(ProvinceDetails, on_delete=models.CASCADE)  # Use ProvinceDetails
    name_en = models.CharField(max_length=100)
    name_si = models.CharField(max_length=100, blank=True)
    name_ta = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'districts'
        ordering = ['name_en']

    def __str__(self):
        return self.name_en


class CityDetails(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    city_district_id = models.ForeignKey(DistrictDetails, on_delete=models.CASCADE,max_length=100,db_column='district_id')  # Use DistrictDetails
    name_en = models.CharField(max_length=100)
    name_si = models.CharField(max_length=100)
    name_ta = models.CharField(max_length=100)
    sub_name_en = models.CharField(max_length=100)
    sub_name_si = models.CharField(max_length=100)
    sub_name_ta = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

    class Meta:
        db_table = 'cities'
        ordering = ['name_en']

    def __str__(self):
        return self.name_en
    
#-------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------- Vehicle Valuation -------------------------------------------------------------------------


class Make(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=30, unique=True)  # Ensure name is unique
    

    class Meta:
        db_table = 'valuation_make'
        ordering = ['name']  # Default ordering by name

    def __str__(self):
        return self.name


class MakeModel(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    

    class Meta:
        db_table = 'valuation_model'
        ordering = ['name']
        
    def __str__(self):
        return self.name


class  vehicle_processed(models.Model):

    url = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    make= models.CharField(max_length=100)
    model= models.CharField(max_length=100)
    year= models.CharField(max_length=100)
    price= models.CharField(max_length=100)
    mileage= models.CharField(max_length=100)
    gear= models.CharField(max_length=100)
    fuel_type= models.CharField(max_length=100)
    engine_capability= models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    date= models.CharField(max_length=100)
    scraped_date= models.CharField(max_length=100)
    store= models.CharField(max_length=100)
    condition= models.CharField(max_length=100)
    
"""
class Meta:
    db_table = 'valuation_model'
    ordering = ['name']
    constraints = [
        models.UniqueConstraint(fields=['name', 'make'], name='unique_make_model')
    ]


class Vehicle(models.Model):
    PURPOSE_SELECT = (
        ('0', 'Selling'),
        ('1', 'Buying'),
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_SELECT, null=False)
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(MakeModel, on_delete=models.SET_NULL, null=True)
    year = models.IntegerField(
        'year',
        choices=year_dropdown,
        validators=[
            MinValueValidator(1900, "Insert a valid year"),
            MaxValueValidator(2030, "Insert a valid year")
        ],
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        make_name = self.make.name if self.make else "Unknown Make"
        model_name = self.model.name if self.model else "Unknown Model"
        return f"{make_name} {model_name} {self.year or 'Unknown Year'}"


class NumberPlate(models.Model):
    PURPOSE_SELECT = [
        ('0', 'Selling'),
        ('1', 'Buying'),
    ]
    
    vehicle_no = models.CharField(max_length=15, unique=True, blank=False)
    purpose = models.CharField(max_length=20, choices=PURPOSE_SELECT, null=False)
    
    def __str__(self):
        return f"{self.vehicle_no} ({self.purpose})"
    

class vehicle_details(models.Model):
    
    url = models.CharField(max_length=100)
    store = models.CharField(max_length=25)
    category = models.CharField(max_length=25)
    make= models.CharField(max_length=25)
    model= models.CharField(max_length=25)
    edition= models.CharField(max_length=25)
    year= models.CharField(max_length=25)
    milage= models.CharField(max_length=25)
    fuel_type= models.CharField(max_length=25)
    gear= models.CharField(max_length=25)
    engine_capacity= models.CharField(max_length=25)
    condition= models.CharField(max_length=25)
    location= models.CharField(max_length=25)
    price= models.CharField(max_length=25)
    options= models.CharField(max_length=25)
    posted_date= models.CharField(max_length=25)
    scraped_date= models.CharField(max_length=25)


    #class Meta:
    #   db_table = 'vehical_data'


    def __str__(self):
        return f"{self.vehicle_no} ({self.purpose})"
    


"""
#-------------------------------------------------------------------------------------------------------------------------------------------