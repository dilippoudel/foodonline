"""This is a custtom user models."""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager)


class UserManager(BaseUserManager):
    """Usermanager to manage the user."""

    def create_user(
            self,
            first_name,
            last_name,
            email,
            username,
            password=None):
        """Create, save and return the user."""
        if not email:
            raise ValueError('Email must be submitted.')
        if not username:
            raise ValueError('User must have username.')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            first_name,
            last_name,
            email,
            username,
            password=None):
        """Create a super user, save and return the user."""
        user = self.create_user(
                email=self.normalize_email(email),
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """User in the system."""
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE,
        blank=True,
        null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    profile_picture = models.ImageField(
        upload_to='users/profile_pictures',
        blank=True,
        null=True)
    cover_photo = models.ImageField(
        upload_to='users/cover_photos',
        blank=True,
        null=True)
    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    country = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    state = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    pin_code = models.CharField(
        max_length=6,
        blank=True,
        null=True)
    latitude = models.CharField(
        max_length=20,
        blank=True,
        null=True)
    longitude = models.CharField(
        max_length=20,
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
