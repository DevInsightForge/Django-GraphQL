from graphene_file_upload.django import FileUploadGraphQLView


class GraphQLView(FileUploadGraphQLView):
    graphiql_template = "apollo/sandbox.html"
