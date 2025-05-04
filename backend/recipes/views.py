from rest_framework import viewsets
from .serializers import RecipeSerializer, IngredientSerializer
from .models import Recipe, Ingredient
from rest_framework import filters
from api.permissions import IsAuthorOrReadOnly
from api.pagination import UserPagination
from django_filters.rest_framework import DjangoFilterBackend


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('^name',)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = UserPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author__id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



