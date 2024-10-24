from django.urls import path
from .views import *
app_name='myapp'
urlpatterns = [
    path('course/', create_course,name = 'coursemodel'),
    path('concept/', create_concept, name = 'conceptmodel'),
    path('menu/', menu, name = 'menu'),
    path('delete/<int:id>', delete, name = 'delete'),
    path('update/<int:id>', update, name = 'update'),
]