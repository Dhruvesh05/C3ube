from django.db import models

class Stock(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='stock_images/')

    def __str__(self):
        return self.name




class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.TextField()  # List of items in the order
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - Total: {self.total_price}"


from django.contrib.auth.models import User

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

