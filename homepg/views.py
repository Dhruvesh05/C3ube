from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
from .forms import StockForm 
import os
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import BillForm


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('pass')  # Ensure this matches your input name
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('billing-page')  # Redirect to insert stock page after login
#         else:
#             messages.error(request, 'Invalid username or password.')
    
#     return render(request, 'login.html')  # Update this to your actual login template


@login_required(login_url='/')
@csrf_exempt


def stock_insert_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        stock = Stock(category=category, name=name, price=price, image=image)
        stock.save()

        return JsonResponse({'message': 'Stock added successfully!'})
    return render(request, 'insert-stock.html')

def get_categories(request):
    categories = Stock.objects.values_list('category', flat=True).distinct()
    return JsonResponse({'categories': list(categories)})

def get_items(request):
    category = request.GET.get('category')
    if category:
        items = Stock.objects.filter(category=category)
    else:
        items = Stock.objects.all()
    
    items_list = [{'name': item.name, 'price': item.price, 'image': item.image.url} for item in items]
    return JsonResponse({'items': items_list})







@login_required(login_url='/')
def billing_page_view(request):
    categories = Stock.objects.values_list('category', flat=True).distinct()
    items = Stock.objects.all()
    return render(request, 'billing-page.html', {'categories': categories, 'items': items})

# AJAX handler to filter items by category
def filter_items_by_category(request, category):
    items = Stock.objects.filter(category=category)
    items_data = [{'name': item.name, 'price': item.price, 'image': item.image.url} for item in items]
    return JsonResponse({'items': items_data})




def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('pass')

            # Create the user using create_user method
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! You can log in now.')  # Display success message
            
        elif action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('billing-page/')  # Redirect to a home page or dashboard after login
            else:
                return HttpResponse("Invalid Password")

    return render(request, 'login.html')

@login_required  # Ensure only logged-in users can access this view
# def billing_page_view(request):
#     user = request.user  # Get the currently logged-in user
#     data = {
#         'username': user.username,  # Access the username from the user object
#         'email': user.email,  # Access the email from the user object
#     }
#     return render(request, 'billing-page.html', data)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')  # Redirect to the home page or login page after logout

def payment_page(request):
    # Initialize an empty bill items and total amount
    bill_items = []
    total_amount = 0

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill_items = form.cleaned_data['bill_items'].split(',')  # Split into a list
            total_amount = form.cleaned_data['total_amount']

            context = {
                'bill_items': bill_items,
                'total_amount': total_amount,
            }
            return render(request, 'payment.html', context)
    else:
        # For GET request, you might want to initialize a form instance
        form = BillForm()

    # If not POST, render the payment page with empty or default values
    context = {
        'bill_items': bill_items,
        'total_amount': total_amount,
    }
    return render(request, 'payment.html', context)  # Render the payment page POST

def help_page(request):
    return render(request, 'help.html')

