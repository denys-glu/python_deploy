from django.db import models
import re
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def register_validator(self, post):
        errors = {}

        # First Name validation
        if len(post['first_name']) < 2:
            errors['first_name'] = "You can make your name better better! like couple more characters!!"
        if len(post['first_name']) > 100:
            errors['first_name'] = "That's kinda to much for your name, slow down buddy!"

        # Last Name validation
        if len(post['last_name']) < 2:
            errors['last_name'] = "Last name is kinda to short"
        if len(post['last_name']) > 100:
            errors['last_name'] = "Last name is way to long"

        # Email validation

        if not self.EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid email address!"

        emails = User.objects.filter(email=post['email'])

        if len(emails) > 0:
            errors['email'] = "This email address is already taken"

        # Password validator
        if len(post['password']) < 8:
            errors['password'] = "PASSWROD SUPOSE TO BE AT LEAST 8 CHARACTERS!!!!!!!!"

        if post['password'] != post['confirm_password']:
            errors['confrim_password'] = "Dude, really? you couldnt type your password twice without mistakes?"

        return errors

    def login_validator(self, post):
        errors = {}

        # Email validation

        if not self.EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid email address!"

        # Password validator
        user = User.objects.filter(email=post['email'])

        if user:
            our_user = user[0]
            print(our_user.email)
            if not bcrypt.checkpw(post['password'].encode(), our_user.password.encode()):
                errors['password'] = "WRONG! YOU WRONG! YOU WRONG!!!!"
        else:
            errors['email'] = "couldnt find that email, is this email valid/registered?"

        return errors

    def update_user_validator(self, post, user_id):
        errors = {}

            # First Name validation
        if len(post['first_name']) < 2:
            errors['first_name'] = "You can make your name better better! like couple more characters!!"
        if len(post['first_name']) > 100:
            errors['first_name'] = "That's kinda to much for your name, slow down buddy!"

        # Last Name validation
        if len(post['last_name']) < 2:
            errors['last_name'] = "Last name is kinda short to short"
        if len(post['last_name']) > 100:
            errors['last_name'] = "Last name is way to long"

        # Email validation

        if not self.EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid email address!"

        user = User.objects.get(id = user_id)
        emails = User.objects.filter(email=post['email'])

        if user.email != post['email']:
            if len(emails) > 0:
                errors['email'] = "This email address is already taken"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
