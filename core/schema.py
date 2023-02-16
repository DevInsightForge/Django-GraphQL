import asyncio
import datetime

import graphene
from graphql import GraphQLError

from account.schema import AuthMutation, AuthQuery


# Root Schema Definitions
class Query(AuthQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


class Subscription(graphene.ObjectType):
    count_seconds = graphene.String(up_to=graphene.Int())

    async def subscribe_count_seconds(self, info, up_to):

        # while True:
        #     yield datetime.datetime.now()
        #     await asyncio.sleep(1)
        for _ in range(up_to):
            time = datetime.datetime.now()
            print("TestSubs: ", time)
            yield time
            await asyncio.sleep(1)


RootSchema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
