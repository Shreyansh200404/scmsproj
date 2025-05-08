from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def home1(request):
    return render(request,'connections/home1.html')




#code
def home(request):
    return render(request, 'connections/home.html')


def customer_registration(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            
            form.save()
            print
            messages.success(request, "Customer registered successfully.")
            customer= Customer.objects.last()
            print(customer)
            conn= Connection(customer=customer)
            form = ConnectionForm(instance=conn)
            return render(request, 'connections/registrationsuccess.html', locals())
        else:
            print(form.errors)
            messages.error(request, "Registration failed. Please correct the errors below.")
    
    form = CustomerForm()
    return render(request, 'connections/customer_registration.html', {'form': form})

def user_registration(request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "User registered successfully. Please log in.")
                return redirect('login')
            else:
                messages.error(request, "Registration failed. Please correct the errors below.")
        else:
            form = UserRegistrationForm()
        return render(request, 'connections/user_registration.html', {'form': form})

def apply_connection(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
           if Customer.objects.filter(user=request.user).exists():
                customer = Customer.objects.get(user=request.user)
                form = ConnectionForm(request.POST, initial={'customer': customer})
                if form.is_valid():
                    form.save()
                    return redirect('home')
           else:
               return redirect('customer_registration')
        else:
            print(form.errors)
            messages.error(request, "Connection application failed. Please correct the errors below.")
            conn= Connection(customer=customer)
            form = ConnectionForm(instance=conn)
            return render(request, 'connections/apply_connection.html', {'form': form})
    else:
        if request.user.is_authenticated:
           if Customer.objects.filter(user=request.user).exists():
                cust= Customer.objects.get(user=request.user)
                conn= Connection(customer=cust)
                form = ConnectionForm(instance=conn)
           else:
               customer = Customer.objects.create(user=request.user,email=request.user.email,name=request.user.username)
               form = CustomerForm(instance=customer)
               return render(request, 'connections/customer_registration.html', {'form': form})
               
        else:
            messages.error(request, "You need to be logged in to apply for a connection.")
            return redirect('login')
    return render(request, 'connections/apply_connection.html', {'form': form})

def connection_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view connections.")
        return redirect('login')
    if not Customer.objects.filter(user=request.user).exists():
        messages.error(request, "You need to register as a customer to view connections.")
        return redirect('customer_registration')
    customer = Customer.objects.get(user=request.user)
    connections = Connection.objects.filter(customer=customer)
    if not connections.exists():
        messages.error(request, "No connections found for this customer.")
        return redirect('home')
    return render(request, 'connections/connection_list.html', {'connections': connections})

def connection_edit(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id)

    if request.method == 'POST':
        
        connection_type = request.POST.get('connection_type')
        status = request.POST.get('status')
        connection.connection_type = connection_type
        connection.status = status
        connection.save()
       
        messages.success(request, "Connection updated successfully.")
        return redirect('dashboard')
       
    else:
        
        
        return render(request, 'connections/connection_edit.html', locals())


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'connections/contact.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another one.")
                return render(request, 'register.html', {'form': form})

            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            else:
                messages.success(request, "Login successful.")
                return redirect('home')
           
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home1')


def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view the dashboard.")
        return redirect('login')
    elif request.user.is_superuser:
        connectionCount = Connection.objects.count()
        customerCount = Customer.objects.count()
        userCount = User.objects.count()
        connections = Connection.objects.all()
    return render(request, 'connections/dashboard.html', locals())