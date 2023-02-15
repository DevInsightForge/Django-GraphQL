import asyncio

import graphene
from graphql import GraphQLError

from account.schema import AuthMutation, AuthQuery


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
            print("TestSubs: ", i)
            yield i
            await asyncio.sleep(1)


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
