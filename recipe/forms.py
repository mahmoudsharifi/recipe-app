from django import forms

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control-lg", "placeholder": "Search for a recipe..."}), required=False)