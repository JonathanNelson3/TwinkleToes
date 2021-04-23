from django.db import models
import re
import bcrypt
from datetime import datetime
from django import forms

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_validator(self, user_data):
        errors = {}
        if len(user_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'     
        if len(user_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        if not EMAIL_REGEX.match(user_data['email']):
            errors['email'] = 'Email format is invalid'
        if self.filter(email = user_data['email']):
            errors['email'] = 'This email address is already in use'
        if len(user_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if user_data['password'] != user_data['confirm']:
            errors['confirm'] = 'Passwords do not match'
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def update_validator(self, user_data):
        errors = {}
        if len(user_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'     
        if len(user_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        if not EMAIL_REGEX.match(user_data['email']):
            errors['email'] = 'Email format is invalid'
        if self.filter(email = user_data['email']):
            errors['email'] = 'This email address is already in use'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class CommentManager(models.Manager):
    def comment_validator(self, comment_data):
        errors = {}
        if len(comment_data['comment']) < 10:
            errors['comment'] = 'Comment must be at least 10 characters'
        if len(comment_data['comment']) < 1:
            errors['comment'] = 'Please enter valid comment'
        return errors

class CommentPost(models.Model):
    poster = models.ForeignKey(
        User,
        related_name = "comments",
        on_delete = models.CASCADE,
        null = True
    )
    comment = models.CharField(max_length = 255, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()
    user_likes = models.ManyToManyField(User, related_name = "liked_comments")