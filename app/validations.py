import os
from django.forms import ValidationError
from datetime import datetime, date
import re


def image_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid = [".jpg", ".jpeg"]
    if ext not in valid:
        raise ValidationError("Unsupported file extension (upload jpg or jpeg files).")


def date_validator(value):
    dob = datetime(value.year, value.month, value.day)
    present = datetime.now()
    if dob > present:
        raise ValidationError("Date of birth needs to be in the past.")


def phone_validator(value):
    is_correct = re.search(r"^07\d{9}$", value)
    if not is_correct:
        raise ValidationError("Telephone is in wrong format.")