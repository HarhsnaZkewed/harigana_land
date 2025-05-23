from django.shortcuts import render, redirect
from .models import PropertyDetails,DistrictDetails,CityDetails
from .models import Make,MakeModel
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
import re
import pymongo
import logging
from pandas import DataFrame
from django.contrib import messages
from django.http import HttpResponseServerError
import pandas as pd
from .models import Feedback  # Assuming you have a Feedback model
from .models import LandValuationFeedback # Assuming you have a Feedback model

#from .dmt_automation import DMTautomation  # Import your automation script




# Configure logging
#logging.basicConfig(level=logging.DEBUG)

"""# Check the connection status
def check_mongo_connection():
    try:
        # Ping the server to check connection
        client.admin.command('ping')
        print("MongoDB is connected.")
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False
    """

#-------------------------------------- Additional DB For vehvile valuations ---------------------------------------------------------------
client = pymongo.MongoClient("mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority", 27017)
DB = client.get_database('data_store_dev')
DB1 = client.get_database('data_store')
#collection = DB.get_collection('vehicle_data_with_details')
collection = DB1.get_collection('processed_data')
collectionfb = DB.get_collection('feedback')
result_collection = DB.get_collection('advanced_valuation_records')
#-------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------- Default Page loads ------------------------------------------------------------------
def home(request):
    
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def valuation_home(request):
    return render(request, 'valuation_home.html')
#-------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------- Land Valuation --------------------------------------------------------------------

def property_view(request):
    # Get all districts
    districts = DistrictDetails.objects.all()
    #cities = []  # Initialize empty city list
    cities = CityDetails.objects.all()

    max_value = 0
    min_value = 0
    avg_value = 0
    avg_rent_value = 0
     

    # Default form data
    form_data = {
        'district': '',
        'city': '',
        'property_type': '',
        'bedrooms': '',
        'bedrooms_check': False,
        'bathrooms': '',
        'bathrooms_check': False,
        'floor_area': '',
        'floor_area_check': False,
        'land_area': '',
        'land_area_check': False,
        'comfort_features': [],
    }

    if request.method == 'POST':
        selected_option = request.POST.get('selected_option','')
                
        if selected_option == 'Dropdown Menu':
                
            # Extract form data
            district_data = request.POST.get('district', '').strip()
            # Split the value to get both parts
            if district_data:
                district_id, district_name = district_data.split(',')
            else:
                district_id, district_name = None, None

            city_data= request.POST.get('city', '').strip()
            if city_data:
                city_id,city_name=city_data.split(',')
            else:
                city_id,city_name = None, None

            map_district = request.POST.get('map_district', '')
            map_city = request.POST.get('map_city', '')

             # Get cities for the selected district
            if district_id:
                district_id = int(district_id)
                #print('district_id:', district_id)
                cities = CityDetails.objects.filter(city_district_id=district_id)
               #print('print2', list(cities))
               

        else:         
            map_district = request.POST.get('map_district', '')
            print(f"map district : {map_district}")
            district_name = map_district

            map_city = request.POST.get('map_city', '')
            print(map_city)
            city_name = map_city

        property_type = request.POST.get('property_type', '').strip()


        #These check fields were used to track wheather the thier respective fields have been changed from 0 
        bedrooms = request.POST.get('bedrooms', '')
        bedrooms_check = request.POST.get('bedrooms_check')
  

        bathrooms = request.POST.get('bathrooms', '')
        bathrooms_check = request.POST.get('bathrooms_check')
        

        floor_area = request.POST.get('floor_area', '')
        #print(floor_area)
        floor_area_check = request.POST.get('floor_area_check')
        

        land_area = request.POST.get('land_area', '')
        #print(land_area)
        land_area_check = request.POST.get('land_area_check')

        comfort_features = request.POST.getlist('feature', [])

        # Update form_data with submitted values
        form_data.update({
                'district': district_name,
                'city': city_name,
                'map_district': map_district,
                'map_city': map_city,
                'property_type': property_type,
                'bedrooms': bedrooms,
                'bedrooms_check': bedrooms_check,
                'bathrooms': bathrooms,
                'bathrooms_check': bathrooms_check,
                'floor_area': floor_area,
                'floor_area_check': floor_area_check,
                'land_area': land_area,
                'land_area_check': land_area_check,
                'comfort_features': comfort_features,
        })    

                       
        """
        # Filter properties based on the form data
        filtered_properties = PropertyDetails.objects.filter(
                Q(location__icontains=district_name) & Q(location__icontains=city_name),
               
            )
        """

        if city_name:
                filtered_properties = PropertyDetails.objects.filter(location__icontains=city_name)

        if filtered_properties:
            rented_propeties = filtered_properties.filter(property_type__icontains='Rental')
            if rented_propeties:  # Check if rented_properties is not empty
                sum_rent_value = sum(
                                        float(re.search(r'\d[\d,\.]*\d', str(property.unit_price)).group(0).replace(',', ''))
                                        for property in rented_propeties
                                            if property.unit_price and re.search(r'\d[\d,\.]*\d', str(property.unit_price))  # Check for valid numeric value
                                        ) 
                avg_rent_value = f"Rs {(sum_rent_value / len(rented_propeties)):,.2f}"
            else:
                avg_rent_value = "RS 0.00"  # Default value if no rented properties found

        if property_type:
            filtered_properties = filtered_properties.filter(property_type__icontains=property_type)

        if int(bedrooms)>0:
            filtered_properties = filtered_properties.filter(bedrooms=int(bedrooms))

        if int(bathrooms)>0:
            filtered_properties = filtered_properties.filter(bathrooms=int(bathrooms))

        if int(floor_area)>0:
            filtered_properties = filtered_properties.filter(floor_area__gte=str(floor_area) )
                    
        if int(land_area)>0:
            filtered_properties = filtered_properties.filter(land_area__gte=int(land_area))

        if comfort_features:
            feature_queries = Q() 
            for feature in comfort_features:
                feature_queries &= Q(property_details__icontains=feature) | Q(property_features__icontains=feature)
            filtered_properties = filtered_properties.filter(feature_queries)

               

            # Extract numeric values safely
        def extract_numeric_value(value):
            match = re.search(r'\d[\d,\.]*\d', str(value))  # Match numbers with optional commas/periods
            if match:
                try:
                     return float(match.group(0).replace(',', ''))  # Remove commas and convert to float
                except ValueError:
                    pass  # Skip invalid numbers
            return None  # Return None if no valid numeric value found
            
        if filtered_properties:
            # Filter out properties with valid numeric unit_price
            numeric_values = [
                extract_numeric_value(property.unit_price)
                for property in filtered_properties
                if property.unit_price and extract_numeric_value(property.unit_price) is not None
            ]

            if numeric_values:  # Ensure there are valid numeric values to process
                max_value = f"RS {max(numeric_values):,.2f}"
                min_value = f"RS {min(numeric_values):,.2f}"
                avg_value = f"RS {sum(numeric_values) / len(numeric_values):,.2f}"
            else:
                max_value = min_value = avg_value = "RS 0.00"  # Handle the case with no valid numbers
        else:
            max_value = min_value = avg_value = "RS 0.00"  # Handle the case with no properties



        prices = {
                'max_value':max_value,
                'min_value':min_value,
                'avg_value':avg_value,
                'avg_rent_value':avg_rent_value,

        }

        context = {
                'records': filtered_properties,
                'form_data': form_data,
                'districts': districts,
                'cities': cities,
                'prices':prices        

        }

        return render(request, 'property_valuation.html', context)
        
        

    else:
        # Handle GET request - fetch all properties
        all_ad_details = []

        # Populate cities if a district is pre-selected
        if form_data['district']:
            cities = CityDetails.objects.filter(district_id=form_data['district'])
            
        max_value = 0
        min_value = 0
        avg_value = 0
        avg_rent_value = 0

        prices = {
            'max_value':max_value,
            'min_value':min_value,
            'avg_value':avg_value,
            'avg_rent_value':avg_rent_value,


        }

        context = {
            'records': all_ad_details,
            'form_data': form_data,
            'districts': districts,
            'cities': cities,
            'prices':prices,
        }

        return render(request, 'property_valuation.html', context)


def get_cities(request, district_id):
    district_id = int(district_id)  # Get district_id directly from the function argument
    
    if district_id:
        cities = CityDetails.objects.filter(city_district_id=district_id).values('id', 'name_en')
        cities_list = [{'id': city['id'], 'name': city['name_en']} for city in cities]
        return JsonResponse({'cities': cities_list})
    else:
        return JsonResponse({'cities': []})
    

def result(request):
    # Assuming you process form and get district and city
    selected_district = request.POST.get('district')
    selected_city = request.POST.get('city')
    
    # Pass these values to the template
    return render(request, 'result.html', {
        'selected_district': selected_district,
        'selected_city': selected_city,
        # Other context data
    })
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------- Vehicle Valuation-------------------------------------------------------------------
def get_models(request, make_id):
    try:
        make_id = int(make_id)
        
        # Debug: Print all related `make` IDs
        all_makes = MakeModel.objects.values_list('make__id', flat=True).distinct()
        #print(f"Available make IDs: {list(all_makes)}")
        
        # Fetch models related to the given make_id
        models = MakeModel.objects.filter(make__id=make_id)
        if not models:
            print(f"No models found for make_id {make_id}")
        
        # Debug: Check queryset content
        #print(f"Queryset for make_id {make_id}: {models}")

        # Prepare models list to return as JSON
        models_list = models.values('id', 'name')
        #print(f"Models for make_id {make_id}: {list(models_list)}")

        return JsonResponse({'models': list(models_list)})
    except MakeModel.DoesNotExist:
        # In case the make_id does not match any models, return an empty list
        print(f"MakeModel with make_id {make_id} does not exist.")
        return JsonResponse({'models': []})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': str(e)})


def vehicle_valuation(request):
    makes = Make.objects.all()
    models = MakeModel.objects.all()
    year_dropdown = [("", "-- Select Year --")] + [(y, y) for y in range(1980, datetime.now().year + 1)]

    form_data = {
        'make': '',
        'model': '',
        'year': '',
        'purpose': '',
    }

    if request.method == 'POST':
        make_data = request.POST.get('make')
        make_id = make_name = None
        if make_data:
            try:
                make_id = int(make_data)  # Ensure this is an integer
                make_name = Make.objects.get(id=make_id).name
            except (ValueError, Make.DoesNotExist):
                make_id = make_name = None

        model_data = request.POST.get('model')
        model_id = model_name = None
        if model_data:
            try:
                model_id = int(model_data)  # Ensure this is an integer
                model_name = MakeModel.objects.get(id=model_id).name
            except (ValueError, MakeModel.DoesNotExist):
                model_id = model_name = None

        year = request.POST.get('year')
        purpose = request.POST.get('purpose')

        mileage = request.POST.get('mileage')
        #print(mileage)
        engine_capacity = request.POST.get('engine_capacity')
        #print(engine_capacity)
        gear = request.POST.get('gear')
        #print(gear)
        fuel = request.POST.get('fuel')
        #print(fuel)
        owners = request.POST.get('owners')
        #print(owners)
        selling_condition = request.POST.get('selling_condition')
        #print(selling_condition)
        modification = request.POST.get('modification')
        #print(modification)

        # Update form_data with selected values
        form_data.update({
            'make': make_id,  # Store `id` for consistency
            'model': model_id,
            'year': int(year),
            'purpose': purpose,
            'mileage':mileage,
            'gear':gear,
            'engine_capacity':engine_capacity,
            'fuel':fuel,
            'owners':owners,
            'selling_condition':selling_condition,
            'modification':modification
        })

        print(make_name, model_name, year)

        # Query with case-insensitive regex
        query = {
            'make': {'$regex': f'^{make_name}$', '$options': 'i'},
            'model': {'$regex': f'^{model_name}$', '$options': 'i'},
            'year': year  # Ensure year matches data type in DB
        }

        if make_name and model_name and year:
            if collection.count_documents(query) == 0:
                print("No matching vehicles found.")
            else:
                if mileage:
                    #query['mileage'] = str(float(mileage))
                    mileage = float(mileage)  # Convert input to float
                    lower_bound = mileage - 5000  # Lower range
                    upper_bound = mileage + 5000  # Upper range

                    query['mileage'] = {"$gte": str(lower_bound), "$lte": str(upper_bound)}


                if engine_capacity:
                    #query['engine_capability'] = str(int(engine_capacity))
                    engine_capability = float(engine_capacity)
                    lower_bound = engine_capability - 100
                    upper_bound = engine_capability + 100

                    query['engine_capability'] = {"$gte": str(lower_bound), "$lte": str(upper_bound)}
          

                    
                if gear:
                    query['gear'] = gear

                if fuel:
                    query['fuel_type'] = fuel

                if owners:
                    query['number_of_owners'] = str(float(owners))

                if selling_condition:
                    query['selling_condition'] = selling_condition

                if modification:
                    query['modification_status'] = modification

                # Run the refined query
                filtered_vehicle_list  = list(collection.find(query))

                if filtered_vehicle_list:
                    
                    df = DataFrame(filtered_vehicle_list)

                    if not df.empty:
                        valuation_amount = round(df['price'].astype(float).mean(), -4)
                        format_valuation_amount = "{:,.2f}".format(valuation_amount)

                        maximum_amount = df['price'].astype(float).max()
                        format_maximum_amount = "{:,.2f}".format(maximum_amount)

                        minimum_amount = df['price'].astype(float).min()
                        format_minimum_amount = "{:,.2f}".format(minimum_amount)

                        vehicle_name = f"{make_name} {model_name} {year}"

                        models = MakeModel.objects.filter(make__id=make_id)

                        stats = {
                            'format_valuation_amount': format_valuation_amount,
                            'format_maximum_amount': format_maximum_amount,
                            'format_minimum_amount': format_minimum_amount,
                            'vehicle_name': vehicle_name,
                            'make': make_name,
                            'model': model_name,
                            'year': year,
                            'purpose': str(purpose)
                        }

                        
                        context = {
                            'records': filtered_vehicle_list,
                            'form_data': form_data,
                            'makes': makes,
                            'models': models,
                            'year_dropdown': year_dropdown,
                            'stats': stats,
                        }

                        return render(request, 'vehicle_valuation.html', context)

        # When no data is found, store session values and redirect
        #messages.error(request, 'Sorry, no data is available for the selected vehicle. So please refer the following car details for your reference')

        request.session['value'] = {
            'make': make_name,
            'make_id': make_id,
            'model': model_name,
            'model_id': model_id,
            'year': year,
            'purpose': purpose,
            'form_data': form_data,
            'year_dropdown': year_dropdown,
        }

        return redirect('vehicle-closest')

    # For GET requests or default fallback
    context = {
            'makes': makes,
            'models': models,
            'year_dropdown': year_dropdown,
            'form_data': form_data,  # Include the empty form_data for GET requests
    }

    return render(request, 'vehicle_valuation.html', context)


def closest(request):
    value = request.session.get('value', None)  # Use get to avoid KeyError
    if not value:
        messages.error(request,"No data in session")
        return redirect('vehicle_valuation')

    makes = Make.objects.all()
    make = value.get("make")
    make_id = value.get("make_id")
    
    models =  MakeModel.objects.all()
    model = value.get("model")
    model_id = value.get("model_id")
    
    form_data = value.get("form_data")

    year_dropdown = value.get("year_dropdown")
    user_year = value.get("year")
    purpose = value.get("purpose")

    if not all([make, model, user_year]):
        messages.error(request,"Incomplete data")
        return redirect('vehicle_valuation')

    try:
        user_year = int(user_year)
    except ValueError:
        messages.error(request,"Invalid year format")
        return redirect('vehicle_valuation')

    vehicle_name = f"{make} {model} {user_year}"
    
    context = {
    }

    # Query the database
    vehicles = collection.find({'make': make, 'model': model})

    df = DataFrame(list(vehicles))

    if df.empty:
        #messages.error(request,"No data found for the given make and model")
        stats = {
                    'vehicle_name': vehicle_name,
                    'make': make,
                    'model': model,
                    'year': user_year,
                    'purpose': str(purpose)
                }
        context = {
            'makes': makes,
            'models': models,
            'year_dropdown': year_dropdown,
            'form_data': form_data,
            'stats': stats,  # Just to test modal logic
            'records': ''  # Make sure it's a falsy value
        }
        return render(request, 'vehicle_valuation.html', context)

    # Ensure the columns exist in the DataFrame
    required_columns = ['year', 'price']
    for column in required_columns:
        if column not in df.columns:
            messages.error(request,f"Missing column: {column}")
            return redirect('vehicle_valuation')

    try:
        # Convert 'year' and 'price' columns to numeric
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Drop rows where 'year' or 'price' are NaN
        df = df.dropna(subset=['year', 'price'])

        # Calculate the absolute difference from user_year
        df['year_diff'] = (df['year'] - user_year).abs()

        # Sort by 'year_diff' to get the closest years
        df = df.sort_values(by='year_diff')

        # Select the closest three distinct years
        closest_years = df['year'].unique()[:3]
        df_closest = df[df['year'].isin(closest_years)]

        # Group by 'year' and calculate mean, min, and max prices
        yearly_stats = df_closest.groupby('year')['price'].agg(['mean', 'min', 'max']).reset_index()

        # Custom rounding to thousands with two decimal places
        def round_to_thousands(value):
            return round(value / 1000) * 1000  # Round to nearest thousand

        # Apply custom rounding and format
        yearly_stats['mean'] = yearly_stats['mean'].apply(lambda x: round_to_thousands(x))
        yearly_stats['min'] = yearly_stats['min'].apply(lambda x: round_to_thousands(x))
        yearly_stats['max'] = yearly_stats['max'].apply(lambda x: round_to_thousands(x))

        # Format the values with two decimal points
        yearly_stats['format_valuation_amount'] = yearly_stats['mean'].map('{:,.2f}'.format)
        yearly_stats['format_minimum_amount'] = yearly_stats['min'].map('{:,.2f}'.format)
        yearly_stats['format_maximum_amount'] = yearly_stats['max'].map('{:,.2f}'.format)

        # Convert to dictionary and pass to context
        context['closest_stats'] = yearly_stats.to_dict(orient='records')
        
        form_data = {
        'make': make_id,  
        'model': model_id,
        'year': int(user_year),
        'purpose': purpose,
        }

        makes = Make.objects.all()
        models = MakeModel.objects.all()
        year_dropdown = [("", "-- Select Year --")] + [(y, y) for y in range(1980, datetime.now().year + 1)]

        
        context['makes'] = makes
        context['models'] = models
        context['year_dropdown'] = year_dropdown
        context['form_data'] = form_data
        context['records'] = vehicles
        
        return render(request, 'vehicle_valuation.html', context)


    except Exception as e:
        messages.error(request,f"An error occurred: {str(e)}")
        return redirect('vehicle_valuation')

    
   
    return render(request, 'vehicle_valuation.html', context)
#-------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------- Feedback ----------------------------------------------------------------------------
def submit_vehicle_feedback(request):
    if request.method == "POST":
        feedback_text = request.POST.get("feedback")
        rating = request.POST.get("rating")
        valuation_make  = request.POST.get("valuation_make")
        valuation_model  = request.POST.get("valuation_model")
        valuation_year  = request.POST.get("valuation_year")
        valuation_purpose  = request.POST.get("valuation_purpose")
        valuation_mileage  = request.POST.get("valuation_mileage")
        valuation_gear  = request.POST.get("valuation_gear")
        valuation_engine_capacity  = request.POST.get("valuation_engine_capacity")
        valuation_fuel  = request.POST.get("valuation_fuel")
        valuation_owners  = request.POST.get("valuation_owners")
        valuation_selling_condition  = request.POST.get("valuation_selling_condition")
        valuation_modification  = request.POST.get("valuation_modification")
        valuation_avg_price = request.POST.get("valuation_avg_price")
        valuation_max_price = request.POST.get("valuation_max_price")
        valuation_min_price = request.POST.get("valuation_min_price")

        if feedback_text and rating:
            Feedback.objects.create(
                text=feedback_text, 
                rating=int(rating),
                valuation_make  = valuation_make,
                valuation_model  = valuation_model,
                valuation_year  = valuation_year,
                valuation_purpose  = valuation_purpose,
                valuation_mileage  = valuation_mileage,
                valuation_gear  = valuation_gear,
                valuation_engine_capacity  = valuation_engine_capacity,
                valuation_fuel  = valuation_fuel,
                valuation_owners  = valuation_owners,
                valuation_selling_condition  = valuation_selling_condition,
                valuation_modification  = valuation_modification,                
                valuation_avg_price=valuation_avg_price,
                valuation_max_price=valuation_max_price,
                valuation_min_price=valuation_min_price
            )
            messages.success(request, "Thank you for your feedback!")

        return redirect('vehicle_valuation')  # Redirect to the main page



def submit_land_feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        valuation_district = request.POST.get('valuation_district')
        valuation_city = request.POST.get('valuation_cityack')
        valuation_map_district = request.POST.get('valuation_map_district')
        valuation_map_city = request.POST.get('valuation_map_city')
        valuation_property_type = request.POST.get('valuation_property_type')
        valuation_bedrooms = request.POST.get('valuation_bedrooms')
        valuation_bathrooms = request.POST.get('valuation_bathrooms')
        valuation_floor_area = request.POST.get('valuation_floor_area')
        valuation_land_area = request.POST.get('valuation_land_area')
        valuation_comfort_features = request.POST.get('valuation_comfort_features')

        valuation_max_value = request.POST.get('land_max_value')
        valuation_avg_value = request.POST.get('land_avg_value')
        valuation_min_value = request.POST.get('land_min_value')
        valuation_avg_rent_value = request.POST.get('land_avg_rent_value')

        # Save feedback
        LandValuationFeedback.objects.create(
            rating=rating,
            feedback=feedback,
            valuation_district = valuation_district,
            valuation_city = valuation_city,
            valuation_map_district = valuation_map_district,
            valuation_map_city = valuation_map_city,
            valuation_property_type = valuation_property_type,
            valuation_bedrooms = valuation_bedrooms,
            valuation_bathrooms = valuation_bathrooms,
            valuation_floor_area = valuation_floor_area,
            valuation_land_area = valuation_land_area,
            valuation_comfort_features = valuation_comfort_features,
            valuation_max_value=valuation_max_value,
            valuation_avg_value=valuation_avg_value,
            valuation_min_value=valuation_min_value,
            valuation_avg_rent_value=valuation_avg_rent_value
        )
        messages.success(request, "Thank you for your feedback!")
        return redirect('property_valuation')  # Redirect to the results page or a thank-you page

    return redirect('home')  # Fallback if accessed without POST
#-------------------------------------------------------------------------------------------------------------------------------------------
