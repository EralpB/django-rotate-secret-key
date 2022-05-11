from django.contrib.sessions.backends.cache import (
    SessionStore as BaseSessionStore
)
from rotatesecretkey.sessions.base import RotateSecretKeyMixIn


class SessionStore(RotateSecretKeyMixIn, BaseSessionStore):
    pass
