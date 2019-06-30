from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.


class NFLMUserManager(BaseUserManager):

    def _create_user(self, username, email, mobile, password, is_staff, is_superuser):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          mobile=mobile,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, mobile, password=None):
        return self._create_user(username,email, mobile, password, False, False)

    def create_superuser(self, username, email, mobile, password):
        return self._create_user(username,email, mobile, password, True, True)


class NFLMUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True, unique=True)
    mobile = models.BigIntegerField(null=False, default="9999999999")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.")

    objects = NFLMUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile',]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' %(self.first_Name,self.last_name)

    def get_short_name(self):
        return '%s' %(self.first_name)


class UserAddress(models.Model):
    user = models.ForeignKey(NFLMUser,related_name="user_addresses", null=True, blank=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    company_name = models.CharField(max_length=30,null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=7)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.get_address()

    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self.country, self.zipcode)

    class Meta:
        ordering = ['-updated', '-timestamp']


class ContactUs(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=150)

    def __unicode__(self):
        return self.name


class Customization(models.Model):
    user = models.ForeignKey(NFLMUser, related_name="user_customization")
    name = models.CharField(max_length=25, null=True, blank=True)
    image = models.ImageField(upload_to='products/customized/', blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class HowToUseVideo(models.Model):
    title = models.CharField(max_length=20, blank=False)
    link = models.URLField(blank=False, null=False)
    description = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
