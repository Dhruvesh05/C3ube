from django.contrib import admin
from django.urls import path
from homepg import views  # Ensure views are imported from homepg

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', views.login_view, name='login'),  # Set the login view as the default
    path('insert-stock/', views.stock_insert_view, name='insert-stock'),
    path('get-categories/', views.get_categories, name='get-categories'),
    path('get-items/', views.get_items, name='get-items'),
    path('billing-page/', views.billing_page_view, name='billing-page'),
    path('filter-items/<str:category>/', views.filter_items_by_category, name='filter-items'), 
    path('logout/',views.logout_view,name='logout'), # For AJAX filtering
    path('payment/', views.payment_page, name='payment'),
    path('help/', views.help_page, name='help'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponse
@login_required  # Ensure only logged-in users can access this view
def billing_page_view(request):
    user = request.user  # Get the currently logged-in user
    data = {
        'username': user.username,  # Access the username from the user object
        'email': user.email,  # Access the email from the user object
    }
    return render(request, 'billing-page.html', data)