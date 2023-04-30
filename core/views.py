from django.http import HttpResponseRedirect
from django.views import View

from graphene_file_upload.django import FileUploadGraphQLView


class RedirectToGraphQL(View):
    def get(self, request, *args, **kwargs):
        gql_endpoint = request.build_absolute_uri("/graphql/")

        return HttpResponseRedirect(gql_endpoint)


class GraphQLView(FileUploadGraphQLView):
    graphiql_template = "apollo/studio.html"
