from django.shortcuts import render
from django import views
from django.views.generic import ListView, DetailView

from recipe.models import Recipe

# Create your views here.
class HomeView(ListView):
    model = Recipe
    template_name = "recipe/recipes_home.html"

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe/recipe_detail.html"