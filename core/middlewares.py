from channels.auth import AuthMiddleware, get_user
from channels.sessions import CookieMiddleware, SessionMiddleware
from graphql_jwt.shortcuts import get_user_by_token
from channels.security.websocket import AllowedHostsOriginValidator
from asgiref.sync import sync_to_async


class WsJwtMiddleware(AuthMiddleware):
    @classmethod
    async def resolve_scope(cls, scope):
        try:
            cookie_token = scope["cookies"]["__token"]
            scope["user"]._wrapped = await sync_to_async(get_user_by_token)(
                cookie_token
            )
        except Exception:
            scope["user"]._wrapped = await get_user(scope)


# Handy shortcut for applying all three layers at once
def WsMiddlewareStack(inner):
    return AllowedHostsOriginValidator(
        CookieMiddleware(SessionMiddleware(WsJwtMiddleware(inner)))
    )
