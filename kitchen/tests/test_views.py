from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType, Dish, Cook

DISH_TYPES_URL = reverse("kitchen:dish-types")
MENU_URL = reverse("kitchen:menu")
COOK_CREATE_URL = reverse("kitchen:create-cooks")
DISH_CREATE_URL = reverse("kitchen:create-dish")


class DishDetailViewTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Test Dish Type")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            years_of_experience=5,
        )
        self.cook = Cook.objects.create(username="testuser1", password="Testpassword123", years_of_experience=5,)
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Lorem ipsum",
            price=10.00,
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.cook)
        self.url = reverse("kitchen:dish-detail", args=[self.dish.pk])

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")

    def test_view_returns_correct_dish(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"], self.dish)


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType, Dish, Cook

class ToggleAssignToDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            years_of_experience=5,
        )
        self.cook = Cook.objects.create(username="testuser12314", password="testpassword", years_of_experience=5)
        self.dish_type = DishType.objects.create(name="Test Dish Type")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Lorem ipsum",
            price=10.00,
            dish_type=self.dish_type,
        )

        self.url = reverse("kitchen:toggle-dish-assign", args=[self.dish.pk])

    def test_toggle_assign_to_dish(self):
        self.client.force_login(self.user)

        # Initially, the cook should have 0 dishes
        self.assertEqual(self.cook.dishes.count(), 0)

        # Assign the dish to the cook
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.cook.refresh_from_db()  # Refresh the cook instance from the database
        self.assertEqual(self.cook.dishes.count(), 0)

        # Toggle the dish assignment
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.cook.refresh_from_db()  # Refresh the cook instance from the database
        self.assertEqual(self.cook.dishes.count(), 0)

    def test_toggle_assign_to_dish_redirect(self):
        self.client.force_login(self.user)

        # Initially, the cook should have 0 dishes
        self.assertEqual(self.cook.dishes.count(), 0)

        # Assign the dish to the cook
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        # Check if the view redirects to the correct dish-detail URL
        expected_url = reverse("kitchen:dish-detail", args=[self.dish.pk])
        self.assertRedirects(response, expected_url)


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPES_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testing123",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

    def test_get_dish_types(self):
        DishType.objects.create(
            name="Test type 1",
        )
        DishType.objects.create(
            name="Test type 2",
        )
        DishType.objects.create(
            name="Test type 3",
        )
        response = self.client.get(DISH_TYPES_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_types"]),
            list(dish_types)
        )
        self.assertTemplateUsed(response, "kitchen/dish_types.html")


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test123124",
            password="14uhd1d1d",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "user1",
            "password1": "12376gsda",
            "password2": "12376gsda",
            "first_name": "Testing name",
            "last_name": "Testing last name",
            "years_of_experience": 5,
        }
        self.client.post(reverse("kitchen:create-cooks"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MENU_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testing123",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

    def test_get_dishes(self):
        self.dish_type1 = DishType.objects.create(
            name="Test 2",
        )

        self.dish_type2 = DishType.objects.create(
            name="Test 2",
        )

        self.cook1 = get_user_model().objects.create_user(
            username="driver1",
            password="tester12",
            years_of_experience=3,
        )

        self.dish1 = Dish.objects.create(
            name="Dish1",
            description="Lorem ipsum dolor sed risus posuere luctus at nulla, hac himenaeos arcu ac nisl scelerisque.",
            price=18.35,
            dish_type=self.dish_type1,
        )

        self.dish1.cooks.set([self.cook1])

        self.dish2 = Dish.objects.create(
            name="Dish2",
            description="Lorem ipsum dolor sed risus posuere luctus at nulla, hac himenaeos arcu ac nisl scelerisque.",
            price=9.35,
            dish_type=self.dish_type2,
        )

        self.dish2.cooks.set([self.cook1])

        response = self.client.get(MENU_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),  # Update the key to match the actual context variable
            list(dishes)
        )
        self.assertTemplateUsed(response, "kitchen/menu.html")
