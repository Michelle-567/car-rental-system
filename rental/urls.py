# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('cars/', views.car_list, name='car_list'),
#     path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
#     path('signup/', views.signup, name='signup'),
# ]

# rental/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),

    # Auth paths
    path('about/', views.about, name='about'),
    # path('login/', auth_views.LoginView.as_view(template_name='rental/login.html'), name='login'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),  # ✅ THIS IS IMPORTANT
    path('receipt/<int:rental_id>/', views.rental_receipt, name='rental_receipt'),
    path('return/<int:rental_id>/', views.return_car, name='return_car'),
    # rental/urls.py
    path('pay/<int:rental_id>/', views.pay_rental, name='pay_rental'),
    # rental/urls.py
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pay/<int:rental_id>/', views.mark_as_paid, name='mark_as_paid'),
    path('mpesa/stk-push/', views.mpesa_stk_push, name='mpesa_stk_push'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('contact/', views.contact_view, name='contact'),




]


# urlpatterns = [
#     path('cars/', views.car_list, name='car_list'),
#     path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
#     path('receipt/<int:rental_id>/', views.rental_receipt, name='rental_receipt'),
#     path('return/<int:rental_id>/', views.return_car, name='return_car'),
#     path('my-rentals/', views.my_rentals, name='my_rentals'),
# ]
