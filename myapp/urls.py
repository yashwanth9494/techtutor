from django.urls import path
from .views import *

app_name='myapp'

urlpatterns = [
    path('course/', create_course,name = 'coursemodel'),
    path('concept/', create_concept, name = 'conceptmodel'),
    path('menu/', menu, name = 'menu'),
    path('delete/<int:id>/', delete, name = 'delete'),
    path('update/<int:id>/', update, name = 'update'),
    path('menuconcepts/', menuconcepts, name='menuconcepts'),
    path('remove/<int:id>/', remove, name='remove'),
    path('update/<int:id>', updateconcept, name='updateconcept'),
    path('userdata/',UsersData.as_view(),name='userdata'),
    path('usercreate/', user_create, name='usercreate'),
    path('userupdate/<int:id>/', user_update, name='userupdate'),
    path('userdelete/<int:id>/', user_delete, name='userdelete'),
]