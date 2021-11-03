from django.contrib.sessions.backends.cached_db import (
    SessionStore as BaseSessionStore
)
from rotatesecretkey.sessions.base import RotateSecretKeyMixIn


class SessionStore(RotateSecretKeyMixIn, BaseSessionStore):
    pass
