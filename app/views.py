from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .forms import FoodForm
from .models import FavouriteFood
from .decorators import require_auth, require_admin
from .helpers import (
    generate_forms_to_complete,
    update_food_record,
)


@require_http_methods(["GET"])
@require_auth(redirect_view="login")
def home(request):

    if request.user.is_superuser:
        return render(request, "admin_dashboard.html", {})

    else:

        assigned_food_forms = FavouriteFood.objects.filter(
            user=request.user, completed=False
        )

        forms_to_complete = generate_forms_to_complete(
            assigned_food_forms=assigned_food_forms, user=request.user
        )

        context = {"forms": forms_to_complete}

        return render(request, "user_dashboard.html", context)


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, ("Invalid credentials!"))
            return redirect("login")

        login(request, user)
        messages.success(request, ("You Have Been Logged In!"))
        return redirect("home")

    else:
        return render(request, "login.html", {})


@require_http_methods(["POST"])
@require_auth()
def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out!"))
    return redirect("/")


@require_http_methods(["GET"])
@require_auth(redirect_view="login")
@require_admin()
def display_users(request):

    users = User.objects.all().exclude(is_superuser=True)

    context = {
        "user_instances": users,
    }

    return render(request, "users.html", context)


@require_http_methods(["POST"])
@require_auth(message="Please login in!")
@require_admin()
def assign_forms(request, pk=None):

    if pk:

        user = User.objects.filter(pk=pk).first()

        if not user:
            return HttpResponse("User not found", status=400)

        assigned_food_form = FavouriteFood(user=user)
        assigned_food_form.save()

        messages.success(
            request,
            ("Forms were successfully assigned to {}.".format(user.username)),
        )

        return redirect("users")

    return HttpResponse("user id is required", status=400)


@require_http_methods(["POST"])
@require_auth(message="Please login in!")
def complete_forms(request, assigned_form_id=None):

    if assigned_form_id:

        submitted_form = FoodForm(request.POST, request.FILES)

        if not submitted_form.is_valid():
            messages.error(request, submitted_form.errors)
            return redirect("/dashboard")

        food = FavouriteFood.objects.filter(pk=assigned_form_id).first()

        if not food:
            return HttpResponse("No assigned form was found!", status=400)

        if food.completed:
            return HttpResponse("This form has already been compeleted!", status=400)

        if food.user != request.user:
            return HttpResponse("Unauthorized!", status=401)

        update_food_record(
            submitted_form=submitted_form, user=request.user, record_id=assigned_form_id
        )

        messages.success(request, ("You have successfully completed the form."))
        return redirect("/dashboard")

    return HttpResponse("form id is required!", status=400)


@require_http_methods(["GET"])
@require_auth(redirect_view="login")
def history(request):

    if request.user.is_superuser:
        foods = FavouriteFood.objects.filter(completed=True)

    else:
        foods = FavouriteFood.objects.filter(user=request.user, completed=True)

    context = {"foods": foods}

    return render(request, "history.html", context)
