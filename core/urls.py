"""core URL Configuration

"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

from core.views import GraphQLView, RedirectToGraphQL


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=settings.DEBUG))),
    ),
    path("", RedirectToGraphQL.as_view()),
]

if not settings.ON_PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
