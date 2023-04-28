from django.http import HttpResponseRedirect
from django.views import View


class ApolloSandbox(View):
    def get(self, request, *args, **kwargs):
        gql_endpoint = f"{request.scheme}://{request.get_host()}/graphql/"
        studio_url = "https://studio.apollographql.com/sandbox/explorer"

        return HttpResponseRedirect(f"{studio_url}?endpoint={gql_endpoint}")
