from django.db import models

# Create your models here.
class Recipe(models.Model):
    cuisine_choices = [
        ('American', 'American'),
        ('Chinese', 'Chinese'),
        ('French', 'French'),
        ('Italian', 'Italian'),
        ('Japanese', 'Japanese'),
        ('Korean', 'Korean'),
        ('Mexican', 'Mexican'),
        ('Thai', 'Thai'),
        ('Vietnamese', 'Vietnamese'),
        ('Other', 'Other')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    time = models.IntegerField()
    cuisine = models.CharField(max_length=255, choices=cuisine_choices)
    image = models.ImageField(default="removed.png")
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')

    def isValid(self):
        return self.name != "" and self.description != "" and self.time > 0  and self.cuisine != ""
    
    def __str__(self):
        return f"Recipe: {self.name}"
    
    def get_absolute_url(self):
        return f"/recipe/{self.id}/"

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def isValid(self):
        return self.name != "" and self.unit != ""
    
    def __str__(self):
        return f"Ingredient: {self.name} - Unit: {self.unit}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def isValid(self):
        return self.recipe != "" and self.ingredient != "" and self.amount > 0
    
    def __str__(self):
        return f"Recipe: {self.recipe} - Ingredient: {self.ingredient} - Amount: {self.amount}"