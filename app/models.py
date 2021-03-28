from django.db import models
from django.contrib.auth.models import User


class FavouriteFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to="uploads/", blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    food = models.CharField(max_length=100, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.id,)
