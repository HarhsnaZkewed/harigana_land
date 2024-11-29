from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.name_en