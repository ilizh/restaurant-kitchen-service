from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from kitchen.models import DishType, Dish, Cook


# Create your tests here.
class DishTypeModelTest(TestCase):
    def test_str_representation(self):
        dish_type = DishType(name="Main Course")
        self.assertEqual(str(dish_type), "Main Course")


class CookModelTest(TestCase):
    def test_str_representation(self):
        cook = Cook(username="chef_john", first_name="John", last_name="Doe", years_of_experience=5)
        self.assertEqual(str(cook), "chef_john (John Doe)")

    def test_years_of_experience_validation(self):
        with self.assertRaises(ValidationError):
            cook = Cook(username="new_chef", first_name="New", last_name="Chef", years_of_experience=0)
            cook.full_clean()


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Appetizer")
        self.cook = Cook.objects.create(username="master_chef", first_name="Master", last_name="Chef",
                                        years_of_experience=10)

    def test_str_representation(self):
        dish = Dish(name="Spaghetti Carbonara", description="Classic Italian pasta dish", price=12.99,
                    dish_type=self.dish_type)
        self.assertEqual(str(dish), "Spaghetti Carbonara")

    def test_cooks_relationship(self):
        dish = Dish.objects.create(name="Pancakes", description="Fluffy pancakes", price=8.99,
                                   dish_type=self.dish_type)
        dish.cooks.set([self.cook])
        self.assertEqual(dish.cooks.count(), 1)
        self.assertEqual(dish.cooks.first(), self.cook)

    def test_price_decimal_places(self):
        with self.assertRaises(ValidationError):
            dish = Dish(name="Pizza", description="Delicious pizza", price=19.12, dish_type=self.dish_type)
            dish.full_clean()
