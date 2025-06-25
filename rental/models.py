from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    CATEGORY_CHOICES = [
        ('budget', 'Budget'),
        ('midrange', 'Midrange'),
        ('premium', 'Premium/SUV'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='car_images/')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='budget')
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name


# class Rental(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     returned = models.BooleanField(default=False)
#     paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.car.name}"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100, null=True, blank=True) 
    is_active = models.BooleanField(default=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    returned = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.car.name} rented by {self.user.username}"

   

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

