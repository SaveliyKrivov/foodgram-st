from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator

class Ingredient(models.Model):
    name = models.CharField("Название", max_length=128, unique=True)
    measurement_unit = models.CharField("Единица измерения", max_length=64)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField("Название", max_length=256)
    image = models.ImageField("Фото", upload_to='recipes/')
    text = models.TextField("Описание")
    cooking_time = models.IntegerField("Время приготовления", validators=[MinValueValidator(1)])
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInRecipe')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_amounts')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField("Колчиество", validators=[MinValueValidator(1)])
    
