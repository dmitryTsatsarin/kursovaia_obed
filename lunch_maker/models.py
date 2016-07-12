from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Order(models.Model):
    meal = models.CharField(max_length=250)
    person = models.CharField(max_length=100)
    email = models.EmailField()
    byn = models.FloatField(null=True)
    byr = models.IntegerField(null=True)
    comment = models.CharField(max_length=1000000)

    def __unicode__(self):
        return "{0} {1}".format(self.meal, self.person)
