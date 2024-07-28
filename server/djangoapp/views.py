# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate
from .models import CarMake, CarModel, Dealer, Review
from .populate import initiate  # Asegúrate de importar initiate
from django.http import JsonResponse
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Obtener todos los concesionarios o por estado
# Proporcionar la lista de concesionarios en formato JSON

def get_dealerships(request, state=None):
    if state:
        dealerships = Dealer.objects.filter(state=state)
    else:
        dealerships = Dealer.objects.all()
    dealerships_list = list(dealerships.values('id', 'full_name', 'city', 'state', 'address', 'zip'))
    return JsonResponse(dealerships_list, safe=False)

# Proporcionar los detalles de un concesionario en formato JSON
def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    dealer_data = {
        'id': dealer.id,
        'full_name': dealer.full_name,
        'city': dealer.city,
        'address': dealer.address,
        'zip': dealer.zip,
        'state': dealer.state,
    }
    return JsonResponse(dealer_data)

# Obtener detalles de un concesionario por su ID
#def get_dealer_details(request, dealer_id):
#    if dealer_id:
#        endpoint = f"/fetchDealer/{dealer_id}"
#        dealership = get_request(endpoint)
#        return JsonResponse({"status": 200, "dealer": dealership})
#    else:
#        return JsonResponse({"status": 400, "message": "Bad Request"})

# Obtener reseñas de un concesionario por su ID
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        reviews_list = list(reviews.values('id', 'name', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year', 'sentiment'))
        for review_detail in reviews:
            #response = analyze_review_sentiments(review_detail['review'])
            #print(response+)
            print("adf")
            #review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews + reviews_list})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
#@csrf_exempt  #Esto puede dar problemas
def logout_user(request):
    # Logout the user
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)


@csrf_exempt
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
# Update the `get_dealerships` view to render the index page with a list of dealerships
# Proporcionar la lista de concesionarios en formato JSON
def get_dealerships(request):
    dealerships = Dealer.objects.all()
    dealerships_list = list(dealerships.values('id', 'full_name', 'city', 'state', 'address', 'zip'))
    return JsonResponse(dealerships_list, safe=False)



# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
#@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        if not request.user.is_anonymous:
            try:
                data = json.loads(request.body)
                response = post_review(data)
                return JsonResponse({"status": 200, "message": "Review added successfully"})
            except json.JSONDecodeError:
                return JsonResponse({"status": 400, "message": "Invalid JSON"})
            except Exception as e:
                return JsonResponse({"status": 500, "message": str(e)})
        else:
            return JsonResponse({"status": 403, "message": "Unauthorized"})
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})


def get_dealer(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        dealer_data = {
            'full_name': dealer.full_name,
            'city': dealer.city,
            'address': dealer.address,
            'zip': dealer.zip,
            'state': dealer.state,
        }
        return JsonResponse({'status': 200, 'dealer': dealer_data})
    except Dealer.DoesNotExist:
        return JsonResponse({'status': 404, 'message': 'Dealer not found'})

def get_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id)
    reviews_data = list(reviews.values('name', 'review', 'sentiment', 'car_make', 'car_model', 'car_year'))
    return JsonResponse({'status': 200, 'reviews': reviews_data})