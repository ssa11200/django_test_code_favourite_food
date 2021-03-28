import mock
from django.core.files import File
from ..models import FavouriteFood


def mock_file(file_name):
    file = mock.MagicMock(spec=File, name="FileMock")
    file.name = file_name
    return file


def generate_food_form_values(user, file_name, **kwarg):
    values = {
        "name": "sadegh",
        "email": kwarg["email"] if "email" in kwarg else "test@gmail.com",
        "telephone": kwarg["telephone"] if "telephone" in kwarg else "07400000000",
        "photo": mock_file(file_name),
        "dob": kwarg["dob"] if "dob" in kwarg else "03/28/2010",
        "food": kwarg["food"] if "food" in kwarg else "myfood",
        "assigned_form_id": kwarg["assigned_form_id"]
        if "assigned_form_id" in kwarg
        else "5500",
    }
    return values


def create_completed_food_form(user):
    values = generate_food_form_values(user, "test.jpg")
    del values["assigned_form_id"]

    food = FavouriteFood(
        user=user,
        completed=True,
        **{**values, "photo": "test.jpg", "dob": "2010-03-28"}
    )

    food.save()
    return food
