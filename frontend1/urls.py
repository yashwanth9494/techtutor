from django.urls import path
from .views import *

urlpatterns =[
    path('', gethome, name = 'gethome'),
    path('coursecard/', getcourses, name = 'getcourses'),
    path('register/', registrationview, name = 'register'),
    path('login/', loginview, name = 'login'),
    path('profile/', profile, name = 'profile'),
    path('logout/', logoutview, name = 'logout'),
    path('update/<int:id>/', updateview, name = 'update'),
    path('delete/<int:id>/', deleteview, name = 'delete'),
    path('changepassword/<str:value>/',changepassword, name='changepassword'),
    path('changepassword/',changepassword, name='changepassword_no_value'),
    path('addtocart/<int:id>/', addtocartview, name='addtocartview'),
    path('cartview/', cartview, name='cartview'),
    path('removecartitem/<int:id>/', removecartitem, name='removecartitem'),
    path('checkout/', checkoutview, name="checkout"),
    path('checkout/<int:id>/', checkoutview, name="checkoutwithid"),
    path('enroll/', enroll, name="enroll"),
    path('enroll/<int:id>/', enroll, name="enrollwithid"),
    path('enrolledcourses/',enrolledcourses, name='enrolledcourses'),
]