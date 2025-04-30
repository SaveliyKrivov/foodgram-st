from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import CustomUserCreateSerializer
from users.models import CustomUser
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # Сериализация данных
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
        
    

