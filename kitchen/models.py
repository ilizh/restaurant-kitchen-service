from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class DishType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(blank=False, validators=[
        MinValueValidator(1)
    ])

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="dishes")  # Assuming this is how you have set up the relationship

    def __str__(self):
        return f"{self.name}"