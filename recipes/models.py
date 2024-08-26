from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=225)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    item = models.CharField(max_length=225)
    quantity = models.TextField()


class Steps(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField()


class Comments(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.TextField()
    posted = models.DateTimeField
