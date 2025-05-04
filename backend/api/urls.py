from django.urls import path, include
from rest_framework import routers
from users.views import CustomUserViewSet
from recipes.views import RecipeViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    
]
