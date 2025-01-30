from django.urls import path
from .views import membership_plan_list, membership_plan_add, membership_view_details, user_membership, add_user_membership, user_membership_details

app_name ='membership'

urlpatterns = [
    path('membership_plan_list/', membership_plan_list, name='membership_plan_list'),
    path('membership_plan_add/', membership_plan_add,name='membership_plan_add'),
    path('membership_view_details/<int:pk>/', membership_view_details,name='membership_view_details'),
    path('user_membership/', user_membership,name='user_membership'),
    path('add_user_membership/', add_user_membership,name='add_user_membership'),
    path('user_membership_details/<int:pk>/', user_membership_details,name='user_membership_details'),
]
