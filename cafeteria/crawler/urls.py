from django.urls import path
from .views import *

app_name = "crawler"
urlpatterns = [
    path('dormitory/', OutApply.as_view(), name='out-apply'),
    path('rice/', RestaurantView.as_view(), name='restaurant'),
]
