from django.shortcuts import render, redirect
from django.contrib import messages
from user_app.models import User
from .models import Trip

# Create your views here.

def index(r):
    if not "user" in r.session:
        return redirect("/")

    user = User.objects.get(id = r.session['user'])
    context = {
        "user": user,
        "my_trips": Trip.objects.all()
    }
    
    return render(r, "travels.html", context)

def add_trip(r):
    if not "user" in r.session:
        return redirect("/")

    user = User.objects.get(id = r.session['user'])
    context = {
        "user": user
    }

    return render(r, "add_trip.html", context)

def add_trip_post(r):
    errors = Trip.objects.trip_validator(r.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(r, value, extra_tags = key)

        return redirect("/travels/add_trip")
    
    user = User.objects.get(id = r.session['user'])

    trip = Trip.objects.create(
                        name = r.POST['name'],
                        descr = r.POST['descr'],
                        start_date = r.POST['start_date'],
                        end_date = r.POST['end_date'],
                        initiator = user
                        )
    trip.users.add(user)
    
    return redirect("/travels")

def view_trip(r, trip_id):
    if not "user" in r.session:
        return redirect("/")

    trip = Trip.objects.get(id = trip_id)
    context = {
        "user": User.objects.get(id = r.session['user']),
        "trip": trip
    }
    return render(r, "view_trip.html", context)

def delete_trip(r, trip_id):
    if not "user" in r.session:
        return redirect("/")
    
    trip = Trip.objects.get(id = trip_id)
    trip.delete()
    return redirect('/travels')

def cancel_trip(r, trip_id):
    if not "user" in r.session:
        return redirect("/")

    user = User.objects.get(id = r.session['user'])
    trip = Trip.objects.get(id = trip_id)
    trip.users.remove(user)
    return redirect('/travels')

def join_trip(r, trip_id):
    if not "user" in r.session:
        return redirect("/")

    user = User.objects.get(id = r.session['user'])
    trip = Trip.objects.get(id = trip_id)
    trip.users.add(user)
    return redirect('/travels')