from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.pagination import UserPagination
from .serializers import AvatarSerializer

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
