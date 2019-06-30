from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.core.mail import send_mass_mail,send_mail,mail_admins
from managing_users.models import NFLMUser

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=30,null=True,blank=True)
    image = models.ImageField(upload_to="products/tags/",null=True,blank=True)
    alt_text = models.CharField(max_length=30,default="alt_text")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=30)
    highlights = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=30)
    sale_price = models.DecimalField(decimal_places=2, max_digits=30,null=True, blank=True)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=1)
    occasional = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)
    custom_made = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = ProductManager()

    def __unicode__(self):
        return self.sku

    class Meta:
        unique_together = ('title', 'slug')

    def get_price(self):
        if self.sale_price:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class MetaTag(models.Model):
    product = models.OneToOneField(Product)
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=150)
    keywords = models.CharField(max_length=60)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images")
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title


class StockNotification(models.Model):
    product = models.ForeignKey(Product, related_name="product_stocknotifications")
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product.title


def product_post_save_receiver(sender, instance, *args, **kwargs):
    if instance.stock <= 3:
        mail_admins("Out of Stock Notification for " + instance.title, "Current Quantity is: " + str(instance.stock))
    notifications = StockNotification.objects.filter(product=instance)
    if notifications.count()>0:
        list = []
        for notification in notifications:
            subject = 'In stock Notification from NFLM'
            message = notification.product.title + "is back in stock.Make it yours before it gets sold out."
            from_mail = 'info@nflmnew.co.in'
            to = notification.email
            list.append((subject, message, from_mail, [to]))
        mailtuple = tuple(list)
        send_mass_mail(mailtuple)

post_save.connect(product_post_save_receiver, sender=Product)