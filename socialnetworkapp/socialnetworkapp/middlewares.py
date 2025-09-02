from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from oauth2_provider.models import AccessToken
from esocialnetworkapi.models import User
import datetime

@database_sync_to_async
def get_user_from_oauth_token(token_str):
    try:
        token = AccessToken.objects.get(token=token_str)
        if token.expires < datetime.datetime.now(datetime.timezone.utc):
            return AnonymousUser()
        return token.user
    except AccessToken.DoesNotExist:
        return AnonymousUser()

class OAuthTokenMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token_str = None
        for part in query_string.split("&"):
            if part.startswith("token="):
                token_str = part.split("=")[1]
                break

        if token_str:
            scope["user"] = await get_user_from_oauth_token(token_str)
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
