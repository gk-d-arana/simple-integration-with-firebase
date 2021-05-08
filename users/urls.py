from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name="home_view"),
    path('signup/', signup_view, name="signup_view"),
    path('login/', login_view, name="login_view"),
    path('verify/<int:phone_number>', phone_verification, name='phone_verification'),
]