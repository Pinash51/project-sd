from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, "index.html")

def user_register(request):
    return render(request, "register.html")

def admin_register(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Basic validation
            if not username or not first_name or not last_name or not email or not password or not confirm_password:
                messages.error(request, 'All fields are required.')
                return redirect('/register')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('/register')
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('/register')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
                return redirect('/register')
            
            # Create the user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('/login')
            
        return redirect('/register')
    
    except Exception as e:
        messages.error(request, str(e))
        return redirect('/register')

def user_login(request):
    return render(request, "login.html")

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')
        
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            
            if not user_obj.exists():
                messages.error(request, 'Account Not Found')
                return redirect('/login')  # Change to your login page URL
            
            user_obj = authenticate(username=username, password=password)
            
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/')
            
            messages.error(request, 'Invalid User Name and Password')
            return redirect('/login')  # Change to your login page URL
        
        return render(request, 'login.html')  # Ensure you have a login.html template
    
    except Exception as e:
        messages.error(request, str(e))
        return redirect('/login')  # Change to your login page URL

def admin_logout(request):
    logout(request)
    return redirect('/')  # Redirect to the login page or another appropriate page

def menu(request):
    return render(request, "menu.html")
