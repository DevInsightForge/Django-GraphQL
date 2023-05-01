import asyncio
from channels_graphql_ws import GraphqlWsConsumer
from django.core.exceptions import PermissionDenied
from core.schema import RootSchema


class MyGraphqlWsConsumer(GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = RootSchema

    # Uncomment to send keepalive message every 42 seconds.
    # send_keepalive_every = 42

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True

    async def on_operation(self, *args, **kwargs):
        """New client connection handler."""
        if not self.scope["user"].is_authenticated:
            raise PermissionDenied("You do not have permission to perform this action")
