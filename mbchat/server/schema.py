from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            location=OpenApiParameter.QUERY,
            description="Filter servers by category",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="quantity",
            location=OpenApiParameter.QUERY,
            description="Limit the number of results returned",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="by_user",
            location=OpenApiParameter.QUERY,
            description="Filter servers by user",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name="server_id",
            location=OpenApiParameter.QUERY,
            description="Filter servers by server id",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="with_num_members",
            location=OpenApiParameter.QUERY,
            required=False,
            type=OpenApiTypes.BOOL,
            description="Filter servers by number of members",
        ),
    ],
)
