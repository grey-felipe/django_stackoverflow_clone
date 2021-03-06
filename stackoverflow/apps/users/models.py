from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
import os
import jwt


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, bio='', image='', badge='', password=None, isAdmin=False):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            bio=bio,
            image=image,
            isAdmin=isAdmin,
            badge=badge,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        if not password:
            password = None

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    bio = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    image = models.URLField()
    badge = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'isAdmin': self.isAdmin,
            'exp': int(dt.strftime('%s'))
        }, os.environ['APP_SECRET'], algorithm='HS256')
        return token.decode('utf-8')
