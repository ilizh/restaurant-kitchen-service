from django.contrib.auth import get_user_model
from django.test import TestCase
from kitchen.models import DishType, Dish


# Create your tests here.
class ModelsTests(TestCase):
    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="testing",
            years_of_experience=9,
            first_name="user123",
            last_name="test",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="Dish type 1",
        )
        self.assertEqual(
            str(dish_type),
            f"{dish_type.name}"
        )

    def test_dish_str(self):
        dish_type2 = DishType.objects.create(
            name="Dish type 2",
        )

        cooks = get_user_model().objects.create(
            username="wist",
            years_of_experience=2,
            first_name="Anatoliy",
            last_name="Repov",
        )

        self.dish2 = Dish.objects.create(
            name="Dish2",
            description="Lorem ipsum dolor sed risus posuere luctus at nulla, hac himenaeos arcu ac nisl scelerisque.",
            price=9.35,
            dish_type=dish_type2,
        )

        self.dish2.cooks.set([cooks])

        self.assertEqual(
            str(self.dish2),
            f"{self.dish2.name}"
        )
