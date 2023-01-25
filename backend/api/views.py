from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from .serializers import (TagSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, IngredientSerializer)
from users.serializers import ShortRecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @action(methods=['post', 'delete'], detail=True)
    # def favorite(self, request, pk):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)

    #     if request.method == 'POST':
    #         Favorite.objects.create(user=user, recipe=recipe)
    #         serializer = ShortRecipeSerializer(
    #                      recipe, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if request.method == 'DELETE':
    #         favorite_recipe = Favorite.objects.get(
    #                        user=user, recipe=recipe)
    #         if favorite_recipe:
    #             favorite_recipe.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response(
    #             {'error': 'Рецепт не находится в избранном'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(methods=['post', 'delete'], detail=True)
    # def shopping_cart(self, request, pk):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, pk=pk)

    #     if request.method == 'POST':
    #         ShoppingCart.objects.create(user=user, recipe=recipe)
    #         serializer = ShortRecipeSerializer(
    #                      recipe, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if request.method == 'DELETE':
    #         favorite_recipe = ShoppingCart.objects.get(
    #                        user=user, recipe=recipe)
    #         if favorite_recipe:
    #             favorite_recipe.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response(
    #             {'error': 'Рецепт не находится в избранном'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    def post_delete_action(self, request, pk, field_serializer, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            a = model.objects.create(user=user, recipe=recipe)
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

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        return self.post_delete_action(request, pk, ShortRecipeSerializer,
                                       Favorite)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        return self.post_delete_action(request, pk, ShortRecipeSerializer,
                                       ShoppingCart)
