from django.db import models


class Dishes(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    photo = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dishes'
