from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Flight, User
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
    
def logoutUser(request):
    logout(request)
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
        context={'flight_number': flight_number, 'booked_tickets': booked_tickets}
        return render(request, 'book_ticket.html', context)
    else:
        return redirect('flights')
        
@login_required(login_url='login')   
def flights(request):
    all_flights=Flight.objects.all()
    context={'flights':all_flights}
    return render(request, 'flights.html',context)
    
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