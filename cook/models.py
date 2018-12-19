from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length = 20,null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient',null=True, blank=True)
    steps = models.CharField(max_length = 1000, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    class Meta:
        managed = True

class Ingredient(models.Model):
    name = models.CharField(max_length = 20,null=True, blank=True)
    recipes = models.ManyToManyField(Recipe,null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    class Meta:
        managed = True






