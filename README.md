<div align="center">

# [Flight Ticket Booking App](https://book-flight-tickets.onrender.com)
</div>
Flight Ticket Booking App is a web application designed for users to easily book flights and for administrators to manage flights and bookings.

## Type of Users

- **User**: Regular users who book flights.
- **Admin**: Administrators who manage flights and bookings.

## User Use Cases

- **Login**: Users can log in to their accounts.
- **Sign up**: New users can create accounts.
- **Search for Flights**: Users can search for flights based on date and time.
- **Book Tickets**: Users can book tickets on available flights (assuming the default seat count is 60).
- **My Booking**: Users can view all the bookings made by them.
- **Logout**: Users can log out from their accounts.

## Admin Use Cases

- **Login**: Admins can log in using separate credentials.
- **Add Flights**: Admins can add new flights to the system.
- **Remove Flights**: Admins can remove existing flights from the system.
- **View Bookings**: Admins can view all the bookings based on flight number and time.

All pages within the application are protected, i.e. only logged-in users can access them. This ensures the security and privacy of user data

## Installation

Clone the Repository
```
git clone https://github.com/Tarunvetsa/Flight_Ticket-booking
```

Move to project directory
```
cd flightbooking
```

Create Virtual Environment
```
virtualenv env
```

Activate Virtual Environment
```
source env/bin/activate (For mac/Linux)
venv\Scripts\activate (For Windows)
```

Install the requirements of the project.
```
pip install -r requirements.txt
```

Run the App
```
python manage.py runserver
```

> Then, the development server will be running on yourlocalhost at http://127.0.0.1:8000/

----> Also, you can view the app at link [App](https://book-flight-tickets.onrender.com)
