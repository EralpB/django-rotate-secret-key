from django.contrib.sessions.backends.file import (
    SessionStore as BaseSessionStore
)
from rotatesecretkey.sessions.base import RotateSecretKeyMixIn


class SessionStore(RotateSecretKeyMixIn, BaseSessionStore):
    pass
