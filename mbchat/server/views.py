from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()  # Get all server objects from the database

    @server_list_docs
    def list(self, request):
        """Returns a list of servers based on optional query parameters.

        This method allows filtering and retrieving objects based on the query parameters provided in the `request`.

        Query Parameters:

            -category(str): Filter servers by category name.

            -quantity(int): Limit the number of servers returned (pagination).

            -by_user(bool): Filter servers by the currently authenticated user. Requires authentication.

            -server_id(int): Retrieve a specific server by its ID.

            -with_num_members(bool): Annotate each server with the number of members if set to 'true'.

        request: The Django request object.

        Response: The Django response object returns a serialized list of server objects matching the query parameters.

        Raises:

        AuthenticationFailed: If the 'by_user' or 'server_id' parameter is provided,
        and the user is not authenticated.

        ValidationError: If the 'server_id' parameter cannot be converted to an integer.

        404 Error: If the 'server_id' provided does not correspond to an existing server.

        Example Usage:

        Retrieves a list of gaming servers, limited to 10, where the user is a member, and includes member counts.

            GET /servers/?category=Gaming&quantity=10&by_user=true&with_num_members=true

        Retrieves the server with ID 12345 if it exists.

            GET /servers/?server_id=12345

        Notes:
            - When 'by_user' is provided, authentication is required.
              Unauthenticated users will receive an AuthenticationFailed error.

            - 'server_id' should be a valid integer ID of an existing server.If the server doesn't exist, a 404 error
               is returned.

            - 'quantity' limits the number of results returned, useful for pagination.

            - 'with_num_members' adds a 'num_members' field to each server object if set to 'true'."""
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"
        server_id = request.query_params.get("server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                self.queryset = self.queryset.filter(member=request.user.id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        if server_id:
            if not request.user.is_authenticated:
                try:
                    self.queryset = self.queryset.filter(id=server_id)
                    if not self.queryset.exists():
                        return Response({"error": "Server not found."}, status=404)
                except ValueError:
                    raise ValidationError(detail="invalid Server_id value ", code=400)
            else:
                raise AuthenticationFailed()

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
