from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, first_name="", last_name=""):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        if self.model.objects.filter(username=username).exists():
            raise ValueError("A user with the same username already exists")

        user = self.model(email=email, username=username,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, first_name="", last_name=""):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)

        if self.model.objects.filter(username=username).exists():
            raise ValueError("A user with the same username already exists")

        user = self.model(email=email, is_staff=True, is_superuser=True, username=username, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to'),
        related_name='customuser_set',  # Set the related_name to match CustomUser
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user'),
        related_name='customuser_set',  # Set the related_name to match CustomUser
        related_query_name='user',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.username
