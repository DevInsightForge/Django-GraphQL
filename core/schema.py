import graphene
import asyncio
from account.schema import AuthMutation, AuthQuery
from graphql import GraphQLError

# Root Schema Definitions
class Query(AuthQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    count_seconds = graphene.Int(up_to=graphene.Int())

    async def subscribe_count_seconds(self, info, up_to):
        if up_to > 30:
            raise GraphQLError("Count too high, must be <= 30")

        for i in range(up_to):
            yield i + 1
            await asyncio.sleep(1)


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
