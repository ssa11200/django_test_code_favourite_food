from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .validations import image_validator, date_validator, phone_validator
from .models import FavouriteFood


class FoodForm(forms.ModelForm):

    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
    )

    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )

    telephone = forms.CharField(
        label="Telephone",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Telephone (e.g. 07xxxxxxxxx)",
            }
        ),
        validators=[phone_validator],
    )

    photo = forms.FileField(
        label="Profile Picture",
        widget=forms.FileInput(
            attrs={"class": "form-control", "placeholder": "Profile Picture"}
        ),
        validators=[image_validator],
    )

    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Date of Birth",
            }
        ),
        validators=[date_validator],
    )

    food = forms.CharField(
        label="Favourite Food",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Favourite Food"}
        ),
    )

    assigned_form_id = forms.CharField(
        label="", widget=forms.TextInput(attrs={"type": "hidden"})
    )

    class Meta:
        model = FavouriteFood
        fields = ("name", "email", "telephone", "photo", "dob", "food")
