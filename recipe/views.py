import pandas as pd

from django.shortcuts import redirect, render
from django import views
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from recipe.forms import RecipeSearchForm

from recipe.models import Recipe

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipe/recipes_home.html"

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipe/recipe_detail.html"

class SearchView(LoginRequiredMixin, views.View):
    model = Recipe
    template_name = "recipe/search.html"

    def get(self, request):
        query = request.GET.get("query")
        form  = RecipeSearchForm()
        if not query:
            recipes = Recipe.objects.all()
        else:
            recipes = Recipe.objects.filter(name__icontains=query).all()

        df = pd.DataFrame(recipes.values())


        if not df.empty:
            df.columns = df.columns.str.title()
            df_html = df.to_html(classes="table table-striped table-dark table-hover mt-5", justify="start", index=False, header=True, columns=["Name", "Description", "Cuisine", "Time"])
            return render(request, "recipe/search.html", {"recipes": df_html, "form": form})
        else:
            return render(request, "recipe/search.html", {"form": form, "error_message": "No results found"})

        

class LoginView(views.View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "recipe/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET["next"] if "next" in request.GET else "home")
            else:
                error = "Invalid username or password"

        else:
            error = "Invalid username or password"
        return render(request, "recipe/login.html", {"form": form, "error": error})
    
class LogoutView(views.View):
    def get(self, request):
        logout(request)
        return render(request, "recipe/success.html")