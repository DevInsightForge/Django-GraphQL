import asyncio
import json

from graphene_django.settings import graphene_settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from graphql_jwt.decorators import login_required
from graphene_django.settings import graphene_settings
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

import logging

logger = logging.getLogger(__name__)


class GraphQLWebSocketHandler(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.room_name = "graphql"
        self.room_group_name = f"group_{self.room_name}"
        self.schema = graphene_settings.SCHEMA
        super().__init__(*args, **kwargs)

    async def graphql_send(self, id=None, op_type=None, payload=None):
        message = {
            "id": id,
            "type": op_type,
            "payload": payload,
        }

        try:
            await self.send(text_data=json.dumps(message))

        except ConnectionClosedOK:
            self.close()

        except ConnectionClosedError:
            self.close()

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept(subprotocol="graphql-ws")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        raise StopConsumer()

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        method_name = f"process_{data['type']}"
        if method := getattr(self, method_name, None):
            if method == "process_start":
                asyncio.create_task(method(data))
            else:
                await method(data)

        else:
            logger.info("Unknown OP Type: {}", data)

    async def process_connection_init(self, data):
        await self.graphql_send(op_type="connection_ack")

    async def process_start(self, data):
        op_id = data.get("id")

        result = await self.schema.subscribe(
            data["payload"].get("query"),
            # context=ws.request,
            variables=data["payload"].get("variables"),
            operation_name=data["payload"].get("operationName"),
        )

        if hasattr(result, "__aiter__"):
            async for item in result:
                await self.graphql_send(
                    id=op_id, op_type="data", payload=item.formatted
                )

        elif result.errors:
            await self.graphql_send(id=op_id, op_type="error", payload=result.formatted)

        else:
            await self.graphql_send(id=op_id, op_type="data", payload=result.formatted)

        await self.graphql_send(id=op_id, op_type="complete")
