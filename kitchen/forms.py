from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Cook, Dish, DishType


class DishSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish"
            }
        )
    )


class DishTypeSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish type"
            }
        )
    )


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):
        return check_years_of_experience(self.cleaned_data["years_of_experience"])


def check_years_of_experience(years_of_experience):
    if not isinstance(years_of_experience, int):
        raise ValueError('Input correct value')
    if years_of_experience < 1:
        raise ValidationError('Minimum value for years of experience is 1!')
    return years_of_experience


class DishCreationForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"
