from django.db import models
from django.forms import CharField

class Genre(models.Model):
    name = CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True
    )