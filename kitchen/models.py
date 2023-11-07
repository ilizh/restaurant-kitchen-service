from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class DishType(models.Model):
    name = models.CharField(max_length=63)


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=1, validators=[
        MinValueValidator(1)
    ])


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook)
