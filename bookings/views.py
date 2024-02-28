from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q
from datetime import datetime
from .models import Flight, User, Booking
from .forms import FlightForm, MyUserCreationForm

# Create your views here.

def home(request):
    return render(request, 'home.html')
    
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('flights')
        
    if request.method == 'POST':
        name = request.POST.get('name').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, username=name, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('flights')
        else:
            messages.error(request, 'Username or password does not exist')
        
    context = {'page': page}
    return render(request, 'login.html', context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    request.session.clear()
    return redirect('login')

def register(request):
    form = MyUserCreationForm()
    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('flights')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
              
    return render(request, 'signup.html', {'form': form})
    
@login_required(login_url='login')
def book_ticket(request, flight_number):
    flight = Flight.objects.get(flight_number=flight_number)
    if flight.seats_left > 0:
        flight.booked_seats += 1
        flight.seats_left-=1
        flight.save()
        booked_tickets = flight.booked_seats
        Booking.objects.create(user=request.user, flight=flight, seat_number=booked_tickets)
        context={'flight_number': flight_number, 'booked_tickets': booked_tickets}
        return render(request, 'book_ticket.html', context)
    else:
        return redirect('flights')
        
@login_required(login_url='login')   
def flights(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')

        # Filter flights based on the provided criteria
        filtered_flights = Flight.objects.all()

        if from_date:
            filtered_flights = filtered_flights.filter(departure_date__gte=from_date)
        if to_date:
            filtered_flights = filtered_flights.filter(departure_date__lte=to_date)
        if from_time:
            filtered_flights = filtered_flights.filter(departure_time__gte=from_time)
        if to_time:
            filtered_flights = filtered_flights.filter(departure_time__lte=to_time)

        context = {'flights': filtered_flights}
        return render(request, 'flights.html', context)
    else:
        all_flights = Flight.objects.all()
        context = {'flights': all_flights}
        return render(request, 'flights.html', context)
    
@login_required(login_url='login')
def user_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'user_bookings.html', {'bookings': bookings})
    
@login_required(login_url='login')
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')  # Redirect to a page showing all flights
    else:
        form = FlightForm()
    return render(request, 'add_flight.html', {'form': form})
    
@login_required(login_url='login')
def remove_flight(request, flight_number):
    if request.method == 'POST':
        flight = Flight.objects.get(flight_number=flight_number)
        flight.delete()
        return redirect('flights')
    return render(request, 'flight.html', {'flights': Flight.objects.all()})
    
def search_flights(request):
    if request.method == 'POST':
        flight_id = request.POST.get('flight_id')
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')
        
        if from_time:
            from_time = datetime.strptime(from_time, '%H:%M').time()
        if to_time:
            to_time = datetime.strptime(to_time, '%H:%M').time()

        q_filters = Q()
            
        if flight_id:
            if flight_id != 'All':  
                q_filters &= Q(flight_number=flight_id)
            else:
                flight_numbers = Flight.objects.values_list('flight_number', flat=True)
                q_filters &= Q(flight_number__in=flight_numbers)

        if from_time and to_time:
            q_filters &= Q(departure_time__gte=from_time, departure_time__lte=to_time)
        elif from_time:
            q_filters &= Q(departure_time__gte=from_time)
        elif to_time:
            q_filters &= Q(departure_time__lte=to_time)
        elif not from_time and not to_time:
            from_time='00:00'
            to_time='23:59'
            q_filters &= Q(departure_time__gte=from_time, departure_time__lte=to_time)
            
        searched_flights = Flight.objects.filter(q_filters)

        if flight_id and flight_id != 'All':
            bookings = Booking.objects.filter(flight__flight_number=flight_id)
        else:
            bookings = Booking.objects.filter(flight__departure_time__gte=from_time, flight__departure_time__lte=to_time)

        flights = Flight.objects.all() 
        context = {'flights': flights, 'searched_flights': searched_flights, 'bookings': bookings, 'selected_flight_id': flight_id}
        return render(request, 'search_flights.html', context)

    flights = Flight.objects.all()
    return render(request, 'search_flights.html', {'flights': flights})
