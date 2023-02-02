from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.serializers import ShortRecipeSerializer

from .permissions import AuthorAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags', 'is_in_shopping_cart',
                        'is_favorited')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post_delete_action(self, request, pk, field_serializer, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            model.objects.create(user=user, recipe=recipe)
            serializer = field_serializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            chosen_recipe = model.objects.filter(
                           user=user, recipe=recipe)
            if chosen_recipe:
                chosen_recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Объект не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        return self.post_delete_action(request, pk, ShortRecipeSerializer,
                                       Favorite)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self.post_delete_action(request, pk, ShortRecipeSerializer,
                                       ShoppingCart)

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(total_amount=Sum('amount'))
        shopping_list = 'Cписок покупок:\n' + '\n'.join([
            f'{ingredient["ingredient__name"]}'
            f' - {ingredient["total_amount"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            for ingredient in ingredients
        ])
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
