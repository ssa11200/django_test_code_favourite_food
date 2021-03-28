from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.login_user, name="login"),
    path("dashboard/", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("users/", views.display_users, name="users"),
    path("assign-forms/<int:pk>", views.assign_forms, name="assign_forms"),
    path(
        "complete-forms/<int:assigned_form_id>",
        views.complete_forms,
        name="complete_forms",
    ),
    path("history/", views.history, name="history"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
