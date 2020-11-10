from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.
def index(r):
    return render(r, "login.html")

def register(r):
    errors = User.objects.register_validator(r.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(r, value, extra_tags = key)
        
        return redirect("/")
    
    password = r.POST['password']

    user = User.objects.create(first_name = r.POST['first_name'],
                            last_name = r.POST['last_name'],
                            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
                            email = r.POST['email'])
    
    r.session['user'] = user.id

    return redirect("/travels")

def login(r):
    errors = User.objects.login_validator(r.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(r, value, extra_tags = key)

        return redirect("/")
    
    user = User.objects.filter(email = r.POST['email'])

    if user:
        r.session['user'] = user[0].id
        return redirect('/travels')

    return redirect("/")

def logout(r):
    if not "user" in r.session:
        return redirect("/")

    del r.session['user']
    return redirect("/")