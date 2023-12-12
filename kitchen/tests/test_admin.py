from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test12345",
            years_of_experience=5,
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="driver1",
            password="tester12",
            years_of_experience=5
        )

    def test_cook_years_of_experience_list(self):
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_years_of_experience_detail(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)
