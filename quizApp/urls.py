from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('signup_page/', signup_page, name="signup_page"),
    path('otp_page/', otp_page, name="otp_page"),
    path('profile_page/', profile_page, name="profile_page"),
    path('my_collection/', my_collection, name="my_collection"),
    path('payments/', payments, name="payments"),
    path('security/', security, name="security"),
    path('favourite/', favourite, name="favourite"),

    path('signup/', signup, name="signup"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('signin/', signin, name="signin"),
    path('signout/', signout, name="signout"),
    path('update_profile/', update_profile, name="update_profile"),
    path('profile_image_upload/', profile_image_upload, name="profile_image_upload"),
    path('change_password/', change_password, name="change_password"),
    
    # quiz manage urls
    path('create_quesset/', create_quesset, name="create_quesset"),
    path('delete_quesset/<int:pk>/', delete_quesset, name="delete_quesset"),

    path('add_options/<int:pk>/', add_options, name="add_options"),
]