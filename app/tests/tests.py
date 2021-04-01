from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from ..models import FavouriteFood
from .test_helpers import generate_food_form_values, create_completed_food_form


class TestLoginView(TestCase):
    def setUp(self):
        self.url = "/"  # login page is the index page
        self.clinet = Client()
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()

    def test_successful_login(self):
        response = self.client.post(
            self.url, data={"username": "user", "password": "password"}, follow=True
        )

        self.assertRedirects(
            response,
            "/dashboard/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("You Have Been Logged In!" in message.message)

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "user_dashboard.html")
        self.assertEqual(response.templates[1].name, "base.html")

    def test_failed_login(self):
        response = self.client.post(
            self.url,
            data={"username": "user", "password": "wrongpassword"},
            follow=True,
        )

        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Invalid credentials!" in message.message)

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "login.html")
        self.assertEqual(response.templates[1].name, "base.html")

    def test_redirect_to_dashboard_already_loggedin(self):
        self.client.login(username="user", password="password")
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response,
            "/dashboard/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "user_dashboard.html")
        self.assertEqual(response.templates[1].name, "base.html")


class TestDashboardView(TestCase):
    def setUp(self):
        self.url = "/dashboard/"
        self.clinet = Client()
        self.admin = User(username="admin", is_superuser=True)
        self.admin.set_password("password")
        self.admin.save()
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()

    def test_not_loggedin_redirect_to_login(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_admin_loggin(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "admin_dashboard.html")
        self.assertEqual(response.templates[1].name, "base.html")

    def test_user_loggin(self):
        self.client.login(username="user", password="password")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "user_dashboard.html")
        self.assertEqual(response.templates[1].name, "base.html")

    def test_user_assigned_forms(self):
        assigned_food_form1 = FavouriteFood(user=self.user)
        assigned_food_form1.save()
        assigned_food_form2 = FavouriteFood(user=self.user)
        assigned_food_form2.save()

        self.client.login(username="user", password="password")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        forms = response.context["forms"]
        self.assertEqual(len(forms), 2)


class TestLogoutView(TestCase):
    def setUp(self):
        self.url = "/logout/"
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()

    def test_get_request_not_allowed(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_login_required(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 400)

    def test_successful_logout(self):
        self.client.login(username="user", password="password")
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("You Have Been Logged Out!" in message.message)


class TestDisplayUsersView(TestCase):
    def setUp(self):
        self.url = "/users/"
        self.clinet = Client()
        self.admin = User(username="admin", is_superuser=True)
        self.admin.set_password("password")
        self.admin.save()
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()

    def test_post_request_not_allowed(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_login_is_required(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "login.html")
        self.assertEqual(response.templates[1].name, "base.html")

    def test_admin_is_required(self):
        self.client.login(username="user", password="password")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 401)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "Unauthorized!")

    def test_admin_is_required(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "users.html")
        self.assertEqual(response.templates[1].name, "base.html")
        users = response.context["user_instances"]
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "user")


class TestAssignFormView(TestCase):
    def setUp(self):
        self.clinet = Client()
        self.admin = User(username="admin", is_superuser=True)
        self.admin.set_password("password")
        self.admin.save()
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()
        self.url = "/assign-forms/" + str(self.user.pk)

    def test_pk_not_provided(self):
        response = self.client.get("/assign-forms/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_request_not_allowed(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_login_required(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 400)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "Please login in!")

    def test_admin_required(self):
        self.client.login(username="user", password="password")
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 401)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "Unauthorized!")

    def test_user_for_pk_not_found(self):
        self.client.login(username="admin", password="password")
        random_pk = "44"
        response = self.client.post("/assign-forms/" + random_pk, follow=True)
        self.assertEqual(response.status_code, 400)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "User not found")

    def test_success_request(self):
        self.client.login(username="admin", password="password")
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            "/users/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "users.html")
        self.assertEqual(response.templates[1].name, "base.html")

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "success")

        self.assertTrue(
            "Forms were successfully assigned to {}.".format(self.user.username)
            in message.message
        )


class TestCompleteFormView(TestCase):
    def setUp(self):
        self.clinet = Client()
        self.user = User(username="user")
        self.user.set_password("password")
        self.user.save()
        self.random_user = User(username="random_user")
        self.random_user.set_password("password")
        self.random_user.save()
        self.url = lambda assigned_form_id: "/complete-forms/" + assigned_form_id
        self.random_form_id = "55"

    def test_form_id_not_provided(self):
        response = self.client.get(self.url(""), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_request_not_allowed(self):
        response = self.client.get(self.url(self.random_form_id), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_validate_form(self):
        self.client.login(username="user", password="password")

        values = generate_food_form_values(
            user=self.user,
            file_name="test.txt",
            email="wrong_email",
            telephone="24324234",
            dob="10/03/2025",
        )

        response = self.client.post(
            self.url(self.random_form_id), data=values, follow=True
        )

        self.assertRedirects(
            response,
            "/dashboard/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(
            "Unsupported file extension (upload jpg or jpeg files)." in message.message
        )
        self.assertTrue("Enter a valid email address." in message.message)
        self.assertTrue("Telephone is in wrong format." in message.message)
        self.assertTrue("Date of birth needs to be in the past." in message.message)

    def test_food_for_assigned_form_id_doesnot_exists(self):
        self.client.login(username="user", password="password")

        values = generate_food_form_values(
            user=self.user,
            file_name="test.jpg",
        )

        response = self.client.post(
            self.url(self.random_form_id), data=values, follow=True
        )

        self.assertEqual(response.status_code, 400)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "No assigned form was found!")

    def test_already_completed_form(self):
        self.client.login(username="user", password="password")
        assigned_food_form = FavouriteFood(user=self.user)
        assigned_food_form.save()

        values = generate_food_form_values(
            user=self.user,
            file_name="test.jpg",
        )

        # first form is completed
        self.client.post(self.url(str(assigned_food_form.pk)), data=values, follow=True)

        # another request is made to complete the same form
        response = self.client.post(
            self.url(str(assigned_food_form.pk)), data=values, follow=True
        )

        self.assertEqual(response.status_code, 400)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].decode("utf-8"), "This form has already been compeleted!"
        )

    def test_other_user_not_allowed(self):
        self.client.login(username="random_user", password="password")
        assigned_food_form = FavouriteFood(user=self.user)
        assigned_food_form.save()

        values = generate_food_form_values(
            user=self.user,
            file_name="test.jpg",
        )

        response = self.client.post(
            self.url(str(assigned_food_form.pk)), data=values, follow=True
        )

        self.assertEqual(response.status_code, 401)

        messages = response._container
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].decode("utf-8"), "Unauthorized!")

    def test_successful_complete_form(self):
        self.client.login(username="user", password="password")
        assigned_food_form = FavouriteFood(user=self.user)
        assigned_food_form.save()

        values = generate_food_form_values(
            user=self.user,
            file_name="test.jpg",
        )

        response = self.client.post(
            self.url(str(assigned_food_form.pk)), data=values, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertRedirects(
            response,
            "/dashboard/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("You have successfully completed the form." in message.message)


class TestHistoryView(TestCase):
    def setUp(self):
        self.clinet = Client()
        self.admin = User(username="admin", is_superuser=True)
        self.admin.set_password("password")
        self.admin.save()
        self.user1 = User(username="user1")
        self.user1.set_password("password")
        self.user1.save()
        self.user2 = User(username="user2")
        self.user2.set_password("password")
        self.user2.save()
        self.url = "/history/"

    def test_post_request_not_allowed(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_login_required(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_admin_history(self):
        self.client.login(username="admin", password="password")
        form1 = create_completed_food_form(self.user1)
        form2 = create_completed_food_form(self.user2)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        foods = response.context["foods"]
        self.assertEqual(len(foods), 2)

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "history.html")
        self.assertEqual(response.templates[1].name, "base.html")

    # test the history for user 1
    def test_user_history(self):
        self.client.login(username="user1", password="password")
        form1 = create_completed_food_form(self.user1)
        form2 = create_completed_food_form(self.user2)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        foods = response.context["foods"]
        # user 1 can only see 1 record in the history
        self.assertEqual(len(foods), 1)

        self.assertEqual(len(response.templates), 2)
        self.assertEqual(response.templates[0].name, "history.html")
        self.assertEqual(response.templates[1].name, "base.html")
