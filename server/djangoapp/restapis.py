import requests
import os
from dotenv import load_dotenv
<<<<<<< HEAD
from django.conf import settings
=======
from django.conf import settings #puesto por mi
>>>>>>> 5968e54413d29a960675206d34fbb384069bd1f0
from django.http import JsonResponse

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="https://sentianalyzer.1jv1vr3kppbk.us-east.codeengine.appdomain.cloud/")


#  Add code for get requests to back end
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(e + "Network exception occurred")

#  def analyze_review_sentiments(text):
#  request_url = sentiment_analyzer_url+"analyze/"+text
#  Add code for retrieving sentiments


def analyze_review_sentiments(text):
    request_url = f"{settings.SENTIMENT_ANALYZER_URL}analyze/{text}"
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

#  def post_review(data_dict):
#  Add code for posting review
#  Create a `get_dealer_reviews` method


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def post_review(data_dict):
    request_url = f"{settings.BACKEND_URL}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
<<<<<<< HEAD
    except Exception as e:
        print(e + "Network exception occurred")
=======
    except:
        print("Network exception occurred")
>>>>>>> 5968e54413d29a960675206d34fbb384069bd1f0
