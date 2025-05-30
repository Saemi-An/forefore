from rest_framework.decorators import api_view, permission_classes  # noqa: F401
from rest_framework.permissions import IsAdminUser, IsAuthenticated  # noqa: F401
from rest_framework.response import Response


@api_view(['GET'])
def get_routes(request):
    routes = [
        # {'GET': '/api/cookies'},
    ]

    return Response(routes)
