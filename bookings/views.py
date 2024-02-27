from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Flight, User
from .forms import FlightForm

# Create your views here.

def home(request):
    return render(request, 'home.html')
    
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,"User not found")
        
        user=authenticate(request,email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
        
    context={'page':page}
    return render(request,'base/login_register.html', context)
    
def flights(request):
    all_flights=Flight.objects.all()
    context={'flights':all_flights}
    return render(request, 'flights.html',context)
    
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')  # Redirect to a page showing all flights
    else:
        form = FlightForm()
    return render(request, 'add_flight.html', {'form': form})
    
def remove_flight(request, flight_number):
    if request.method == 'POST':
        flight = Flight.objects.get(flight_number=flight_number)
        flight.delete()
        return redirect('flights')
    return render(request, 'flight.html', {'flights': Flight.objects.all()})