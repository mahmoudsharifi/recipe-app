from django.test import TestCase, Client
from django.contrib.auth.models import User

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


class RecipeViewsTestCase(TestCase):
    def setUp(self):
        Recipe.objects.create(name="test", description="test", time=1, cuisine="American")
        Ingredient.objects.create(name="test", unit="test")
        RecipeIngredient.objects.create(recipe_id=1, ingredient_id=1, amount=1)
        User.objects.create_user(username='test', password='test')

    def test_index(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_recipe_authorized(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/recipe/1/')
        self.assertEqual(response.status_code, 200)

    def test_recipe_unauthorized(self):
        c = Client()
        response = c.get('/recipe/1/')
        self.assertEqual(response.status_code, 302)
        
    def test_get_absolute_url(self):
        test = Recipe.objects.get(name="test")
        self.assertEqual(test.get_absolute_url(), "/recipe/1/")

class SearchViewTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='test', password='test')

    def test_search_authorized(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_unauthorized(self):
        c = Client()
        response = c.get('/search/', {'search': 'test'})
        self.assertEqual(response.status_code, 302)

class ChartsViewTestCase(TestCase):
    def setUp(self) -> None:
        Recipe.objects.create(name="test", description="test", time=1, cuisine="American")
        Ingredient.objects.create(name="test", unit="test")
        RecipeIngredient.objects.create(recipe_id=1, ingredient_id=1, amount=1)
        User.objects.create_user(username='test', password='test')

    def test_charts_authorized(self):
        c = Client()
        c.login(username='test', password='test')
        response = c.get('/charts/')
        self.assertEqual(response.status_code, 200)

    def test_charts_unauthorized(self):
        c = Client()
        response = c.get('/charts/')
        self.assertEqual(response.status_code, 302)