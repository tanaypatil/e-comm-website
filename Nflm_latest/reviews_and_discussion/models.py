from __future__ import unicode_literals
from managing_users.models import NFLMUser
from products.models import Product
from django.db import models

# Create your models here.


class Review(models.Model):
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(NFLMUser, null=True)
    product = models.ForeignKey(Product, related_name="product_reviews")
    pub_date = models.DateTimeField('date published')
    nickname = models.CharField(max_length=20, null=True, default="Anonymous")
    comment = models.TextField(max_length=200, null=False)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.nickname

    def avg_rating(self,product):
        reviews = Review.objects.filter(product = product)
        review_count = reviews.count()
        rating_count = 0
        for review in reviews:
            rating_count+= review.rating
        avg_rating = int(rating_count/review_count)
        return avg_rating


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, related_name="review_images")
    image = models.ImageField(upload_to='reviews/%Y/%m/%d/', null=True, blank=True)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.review.user.username


class Discussion(models.Model):
    user = models.ForeignKey(NFLMUser, null=True)
    product = models.ForeignKey(Product)
    nickname = models.CharField(max_length=20, null=True, default="Anonymous")
    text = models.TextField(max_length=100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.nickname
