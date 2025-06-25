from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Car, Rental
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Car, Rental
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RentalForm
from .forms import ContactForm


def home(request):
    return render(request, 'rental/home.html')

def about(request):
    return render(request, 'rental/about.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'rental/signup.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/car_list.html', {'cars': cars})



from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def rent_car(request, car_id):
    ...
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.car = car
            rental.total_cost = car.daily_rate * (rental.end_date - rental.start_date).days
            rental.save()

            # Send Email Receipt
            subject = f"Car2Go Rental Receipt for {car.name}"
            message = render_to_string('rental/email_receipt.html', {
                'rental': rental
            })
            email = EmailMessage(subject, message, to=[request.user.email])
            email.content_subtype = 'html'
            email.send()

            return redirect('rental_receipt', rental_id=rental.id)



@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'rental/my_rentals.html', {'rentals': rentals})



@staff_member_required
def admin_dashboard(request):
    total_cars = Car.objects.count()
    rented_cars = Rental.objects.filter(status='rented').count()
    available_cars = Car.objects.filter(is_available=True).count()
    rentals = Rental.objects.all()

    return render(request, 'rental/admin_dashboard.html', {
        'total_cars': total_cars,
        'rented_cars': rented_cars,
        'available_cars': available_cars,
        'rentals': rentals,
    })


def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/car_list.html', {'cars': cars})


def rental_receipt(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    return render(request, 'rental/rental_receipt.html', {'rental': rental})

@login_required
def return_car(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.returned = True
    rental.save()
    return redirect('my_rentals')

# rental/views.py
from django.contrib.auth.decorators import login_required


@login_required
def pay_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.paid = True
    rental.save()
    messages.success(request, "Payment successful!")
    return redirect('my_rentals')


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required
def mark_as_paid(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.paid = True
    rental.save()
    return redirect('my_rentals')



@staff_member_required
def admin_dashboard(request):
    total_cars = Car.objects.count()
    total_rentals = Rental.objects.count()
    rented_out = Rental.objects.filter(returned=False).count()
    returned = Rental.objects.filter(returned=True).count()
    paid_rentals = Rental.objects.filter(paid=True).count()
    unpaid_rentals = Rental.objects.filter(paid=False).count()

    context = {
        'total_cars': total_cars,
        'total_rentals': total_rentals,
        'rented_out': rented_out,
        'returned': returned,
        'paid_rentals': paid_rentals,
        'unpaid_rentals': unpaid_rentals,
    }
    return render(request, 'rental/admin_dashboard.html', context)

import base64, requests, datetime
from django.conf import settings
from django.http import JsonResponse

def mpesa_stk_push(request):
    phone = request.GET.get('phone')  # e.g. 2547XXXXXXXX
    amount = request.GET.get('amount')  # e.g. 100

    # Get access token
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = r.json().get('access_token')

    # Timestamp & password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    # STK Push
    stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "CarRental",
        "TransactionDesc": "Payment for car rental"
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    return JsonResponse(response.json())

# rental/views.py (add this too)
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def mpesa_callback(request):
    # You can save the payment status here (success/failure)
    print(request.body)  # Inspect this for full response
    return HttpResponse("Callback received")


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for reaching out! We’ll get back to you soon.')
            return redirect('contact')  # or redirect to a thank-you page
    else:
        form = ContactForm()
    return render(request, 'rental/contact.html', {'form': form})


