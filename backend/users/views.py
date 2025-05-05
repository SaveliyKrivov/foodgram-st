from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.pagination import UserPagination
from .serializers import AvatarSerializer, SubscriptionUserSerializer
from .models import Subscription, CustomUser
from django.shortcuts import get_object_or_404

class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = UserPagination

    @action(methods=["put", "delete"], detail=False, url_path='me/avatar')
    def avatar(self, request):
        user = request.user
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request':request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={'avatar':user.avatar.url},
                status=status.HTTP_200_OK
            )
        if user.avatar:
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False, url_path='subscriptions', permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        followed_users = [sub.following for sub in subscriptions]
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(followed_users, request=request)
        serializer = SubscriptionUserSerializer(
            page, many=True, context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)
    
    @action(methods=['post', 'delete'], detail=True, url_path='subscribe', permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(CustomUser, id=id)
        if request.method == 'POST':
            if Subscription.objects.filter(
                user=user, following=following
                ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if user == following:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            subscription = Subscription.objects.create(user=user, following=following)
            serializer = SubscriptionUserSerializer(
                subscription.following, context={'request': request}
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        subscription = Subscription.objects.filter(user=user, following=following)
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)




