from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes  # noqa: F401
from rest_framework.response import Response

from core.products.models import Cookies

from .serializers import CookiesSerializer

# from rest_framework.permissions import IsAdminUser, IsAuthenticated  # noqa: F401


@api_view(['GET'])
def get_routes(request):
    routes = [
        # {'GET': '/api/cookies'},
    ]

    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAdminUser])   // 어드민에서는 session 기반 인증을 진행하기 때문에 사용 안함
def get_cookie(request, pk):
    cookie = get_object_or_404(Cookies, id=pk)
    serializer = CookiesSerializer(cookie)
    return Response(serializer.data)
