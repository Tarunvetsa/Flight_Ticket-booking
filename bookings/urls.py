from django.urls import path,include
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('',views.home,name="home"),
    path('flights/',views.flights,name="flights"),
    path('add-flight/',views.add_flight,name="add_flight"),
    path('remove-flight/<uuid:flight_number>/', views.remove_flight, name='remove_flight'),
]