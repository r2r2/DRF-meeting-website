from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.contrib.gis.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """ Создает и возвращает пользователя с имэйлом и паролем. """
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    gender_choice = [
        ('M', "Male"),
        ('F', 'Female')
    ]
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True) #, default='static/default_avatar/cool-monkey.jpg')
    gender = models.CharField(choices=gender_choice, max_length=1, default='M')
    first_name = models.CharField(max_length=32, validators=[MinLengthValidator(limit_value=2)])
    last_name = models.CharField(max_length=32, validators=[MinLengthValidator(limit_value=2)])
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField('self', through='Follower', related_name='followers', symmetrical=False)
    adress = models.CharField(max_length=128, null=True, blank=True)
    location = models.PointField(null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name} {self.last_name[:1]}.'


class Follower(models.Model):
    """Model of matching between users"""
    user_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    user_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_2')

    def __str__(self):
        return f'{self.user_1} - {self.user_2}'
