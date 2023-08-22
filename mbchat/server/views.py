from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        # filter server results by category, quantity, user and server id
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"
        server_id = request.query_params.get("server_id")

        if by_user or server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            self.queryset = self.queryset.filter(member=request.user.id)

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        if server_id:
            try:
                self.queryset = self.queryset.filter(id=server_id)
                if not self.queryset.exists():
                    return Response({"error": "Server not found."}, status=404)
            except ValueError:
                raise ValidationError(detail="Server value error", code=403)

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
