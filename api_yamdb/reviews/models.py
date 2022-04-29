from django.db import models
from django.forms import CharField


class Genre(models.Model):
    name = CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True
    )
