from django.urls import path, include
from . import views
from rest_framework import routers

# Create a router and register our ViewSets with it.


router = routers.DefaultRouter()
router.register(r'booking', views.BookingViewset, basename='booking')
router.register(r'review', views.ReviewViewset, basename='review')
router.register(r'listing', views.ListingViewset, basename='listing')
router.register(r'payment', views.PaymentViewset, basename='payment')


urlpatterns =[
    # path('')

]+router.urls