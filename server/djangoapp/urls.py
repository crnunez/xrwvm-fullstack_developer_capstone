# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
       path('login', view=views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration, name='register'),
    path('get_cars', view=views.get_cars, name='getcars'),
    path('get_dealers', view=views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path('reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', view=views.add_review, name='add_review'),
    path('dealers/', view=views.get_dealerships, name='get_dealerships'),
    path('dealer/<int:dealer_id>/', view=views.dealer_detail, name='dealer_detail'),
    path('reviews/dealer/<int:dealer_id>/', view=views.get_reviews, name='get_reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
