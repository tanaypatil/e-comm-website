from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from managing_users.models import NFLMUser
from products.models import Tag

from django.db import models

# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(NFLMUser, related_name="user_blog")
    title = models.CharField(max_length=80)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    tags  = models.ManyToManyField(Tag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})


class BlogMetaTag(models.Model):
    blog = models.OneToOneField(Blog, related_name="blog_metatag")
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=160)
    keywords = models.CharField(max_length=160)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.blog.title


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name="blog_images")
    image = models.ImageField(upload_to='blog/images/')
    alt_text = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.blog.title
