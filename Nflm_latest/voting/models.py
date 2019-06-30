from django.db import models


class Pairs(models.Model):
    pid = models.CharField(max_length=10, blank=False, null=True, unique=True, help_text="ID of a pair. Should be unique integer and in order.")
    img1 = models.ImageField(blank=False, null=True, upload_to='voting/images')
    alt_1 = models.CharField(max_length=20, blank=False, null=True, unique=True)
    a1 = models.CharField(max_length=40, blank=False, null=True, unique=True, help_text="First Design submitted by.")
    s1 = models.IntegerField(default=0)
    img2 = models.ImageField(blank=False, null=True, upload_to='voting/images')
    alt_2 = models.CharField(max_length=20, blank=False, null=True, unique=True)
    a2 = models.CharField(max_length=40, blank=False, null=True, unique=True, help_text="Second Design submitted by.")
    s2 = models.IntegerField(default=0)

    def __str__(self):
        return self.pid

    def __unicode__(self):
        return self.pid

    class Meta:
        verbose_name = 'VotingPair'
        verbose_name_plural = 'VotingPairs'
        ordering = ['pid']
