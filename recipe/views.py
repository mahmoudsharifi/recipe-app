import pandas as pd
import matplotlib.pyplot as plt

from django.shortcuts import redirect, render
from django import views
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from recipe.forms import RecipeSearchForm

from recipe.models import Recipe, RecipeIngredient
from recipe.utils import get_chart

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
            table_html = '<table class="table table-striped table-dark table-hover mt-5">'
            table_html += '<thead><tr><th>Name</th><th>Description</th><th>Cuisine</th><th>Time</th></tr></thead>'
            table_html += '<tbody>'
            for index, row in df.iterrows():
                table_html += '<tr>'
                table_html += f'<td><a href="{reverse("recipe_detail", args=[row["Id"]])}" class="link-warning">{row["Name"]}</a></td>'
                table_html += f'<td>{row["Description"]}</td>'
                table_html += f'<td>{row["Cuisine"]}</td>'
                table_html += f'<td>{row["Time"]}</td>'
                table_html += '</tr>'
            table_html += '</tbody></table>'
            return render(request, "recipe/search.html", {"recipes": table_html, "form": form})
        else:
            return render(request, "recipe/search.html", {"form": form, "error_message": "No results found"})

class ChartsView(LoginRequiredMixin, views.View):
    template_name = "recipe/charts.html"

    def get(self, request):
        plt.switch_backend('AGG')
        fig=plt.figure(figsize=(6,3))

        # Create pie chart of the cuisines
        recipes = Recipe.objects.all()
        df = pd.DataFrame(recipes.values())
        df = df["cuisine"].value_counts()
        plt.pie(df, labels=df.index, autopct='%1.1f%%')

        pie_chart = get_chart()
        plt.clf()

        # Create a bar chart of the ingredients in all recipes
        # recipes = RecipeIngredient.objects.all().values("ingredient_id")
        # df = pd.DataFrame(recipes.values())
        # df = df["ingredient_id"].value_counts()
        plt.bar(df.index, df)

        bar_chart = get_chart()
        plt.clf()

        # Create a line chart of the time it takes to make each recipe
        # recipes = Recipe.objects.all()
        # df = pd.DataFrame(recipes.values())
        # df = df["time"].value_counts().sort_index()
        df = df.sort_index()
        plt.plot(df.index, df)

        line_chart = get_chart()
        plt.clf()

        return render(request, "recipe/charts.html", {
            "pie_chart": pie_chart,
            "bar_chart": bar_chart,
            "line_chart": line_chart

        })

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