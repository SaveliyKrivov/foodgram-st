from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Ingredient, Recipe, IngredientInRecipe, Favorite, ShoppingCart
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('id',)

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    
    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(source='ingredient_amounts', many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('id', 'author', 'is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient_amounts')
        recipe = Recipe.objects.create(**validated_data)
        self._set_ingredients(recipe, ingredient_data)
        return recipe
    
    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredient_amounts', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if ingredient_data is not None:
            instance.ingredient_amounts.all().delete()
            self._set_ingredients(instance, ingredient_data)
        return instance

    def _set_ingredients(self, recipe, ingredient_data):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredient_data
        ])

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(
            user=request.user.id,
            recipe=obj
            ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return ShoppingCart.objects.filter(
            user = request.user.id,
            recipe = obj
        ).exists()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url
        return representation
    

        

