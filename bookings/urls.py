from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('admin-login/',views.admin_login,name='admin_login'),
    path('register/',views.register,name='register'),
    path('my-bookings/',views.user_bookings,name='my_bookings'),
    path('search-flights/',views.search_flights,name='search_flights'),
    path('book-ticket/<uuid:flight_number>/',views.book_ticket,name='book_ticket'),
    path('flights/',views.flights,name="flights"),
    path('add-flight/',views.add_flight,name="add_flight"),
    path('remove-flight/<uuid:flight_number>/', views.remove_flight, name='remove_flight'),
]