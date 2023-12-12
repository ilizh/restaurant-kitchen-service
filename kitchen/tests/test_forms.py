from django.core.exceptions import ValidationError
from django.test import TestCase
from kitchen.forms import CookCreationForm, check_years_of_experience
from kitchen.models import Cook, Dish, DishType


class FormsTest(TestCase):
    def test_check_valid_creation_form(self):
        data1 = {
            "username": "user1",
            "password1": "12376gsda",
            "password2": "12376gsda",
            "first_name": "Testing name",
            "last_name": "Testing last",
            "years_of_experience": 7,
        }
        form = CookCreationForm(data=data1)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data1)


class CheckYearsOfExperienceTestCase(TestCase):
    def test_valid_input(self):
        result = check_years_of_experience(5)
        self.assertEqual(result, 5)

    def test_minimum_valid_input(self):
        result = check_years_of_experience(1)
        self.assertEqual(result, 1)

    def test_invalid_negative_input(self):
        with self.assertRaises(ValidationError) as context:
            check_years_of_experience(-3)
        self.assertEqual(str(context.exception), "['Minimum value for years of experience is 1!']")

    def test_invalid_zero_input(self):
        with self.assertRaises(ValidationError) as context:
            check_years_of_experience(0)
        self.assertEqual(str(context.exception), "['Minimum value for years of experience is 1!']")

    def test_invalid_non_integer_input(self):
        with self.assertRaises(ValueError) as context:
            check_years_of_experience("five")
        self.assertEqual(str(context.exception), "Input correct value")
