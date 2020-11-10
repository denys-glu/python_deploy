from django.db import models
from user_app.models import User
import datetime
# Create your models here.

class TripManager(models.Manager):
    def trip_validator(self, post):
        errors = {}

        if len(post['name']) == 0:
            errors['name'] = "Trip name cant be empty"
        elif len(post['name']) > 50:
            errors['name'] = "Trip name cant be more than 50 letters long"

        if len(post['descr']) == 0:
            errors['descr'] = "Description cant be empty"
        elif len(post['descr']) > 150:
            errors['descr'] = "Description cant be more than 150 letters long"

        try:# Start date should be in the future
            if datetime.datetime.strptime(post['start_date'], "%Y-%m-%d").date() <= datetime.datetime.now().date():
                errors['start_date'] = "Start date should be in the future"
        except:
                errors['start_date'] = "Somtehing wrong with you start date"

        try:# End date should be after Start date
            if datetime.datetime.strptime(post['end_date'], "%Y-%m-%d").date() <= datetime.datetime.strptime(post['start_date'], "%Y-%m-%d").date():
                errors['end_date'] = "End date should be after Start date"
        except:
            errors['end_date'] = "Somtehing wrong with you end date"

        return errors

class Trip(models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    initiator = models.ForeignKey(User, related_name="my_trip", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()