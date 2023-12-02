from django.test import TestCase

# Create your tests here.

from .models import Recipe, Ingredient, RecipeIngredient

class RecipeTestCase(TestCase):
    def setUp(self):
        Recipe.objects.create(name="test", description="test", time=1, cuisine="American")
        Ingredient.objects.create(name="test", unit="test")
        RecipeIngredient.objects.create(recipe_id=1, ingredient_id=1, amount=1)

    def test_recipe(self):
        test = Recipe.objects.get(name="test")
        self.assertTrue(test.isValid())

        self.assertEqual(test.name, "test")
        self.assertEqual(test.description, "test")
        self.assertEqual(test.time, 1)
        self.assertEqual(test.cuisine, "American")

    def test_ingredient(self):
        test = Ingredient.objects.get(name="test")
        self.assertTrue(test.isValid())

        self.assertEqual(test.name, "test")
        self.assertEqual(test.unit, "test")

    def test_recipe_ingredient(self):
        test = RecipeIngredient.objects.get(recipe_id=1)
        self.assertTrue(test.isValid())

        self.assertEqual(test.recipe.id, 1)
        self.assertEqual(test.ingredient.id, 1)
        self.assertEqual(test.amount, 1)
