"""core URL Configuration

"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_file_upload.django import FileUploadGraphQLView as GraphQLView
from core.views import ApolloSandbox


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    path("", ApolloSandbox.as_view()),
]
