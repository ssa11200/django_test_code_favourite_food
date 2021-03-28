from django.http import HttpResponse
from .forms import FoodForm


def generate_forms_to_complete(assigned_food_forms, user):
    forms_to_complete = []

    initial = {
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
    }

    for form in assigned_food_forms:

        initial = {**initial, "assigned_form_id": form.pk}
        forms_to_complete.append(FoodForm(instance=form, initial=initial))

    return forms_to_complete


def update_food_record(submitted_form, record_id, user):
    food = submitted_form.save(commit=False)
    food.id = record_id
    food.completed = True
    food.user_id = user
    food.save()
