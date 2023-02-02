from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = self.request.user
        followings = User.objects.filter(following__user=user).all()
        serializer = SubscriptionSerializer(
            followings, many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                         author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                           user=user, author=author)
            if subscription:
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Вы не подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
