import django
from django.conf import settings
from django.contrib.sessions.backends.signed_cookies import (
    SessionStore as BaseSessionStore
)
from django.core import signing
from rotatesecretkey.sessions.base import RotateSecretKeyMixIn


class SessionStore(RotateSecretKeyMixIn, BaseSessionStore):
    def load(self):
        """
        Load the data from the key itself instead of fetching from some
        external data store. Opposite of _get_session_key(), raise
        BadSignature if signature fails.
        """
        serializer = self.serializer
        if django.VERSION > (2, 2):
            max_age = settings.SESSION_COOKIE_AGE
        else:
            max_age = self.get_session_cookie_age()

        def load(key):
            return signing.loads(
                self.session_key,
                key=key,
                serializer=serializer,
                # This doesn't handle non-default expiry dates, see #19201
                max_age=max_age,
                salt='django.contrib.sessions.backends.signed_cookies',
            )
        try:
            return load(key=None)
        except Exception:
            old_key = getattr(settings, 'OLD_SECRET_KEY', None)
            if old_key:
                try:
                    return load(key=old_key)
                except Exception:
                    self.create()
            else:
                # BadSignature, ValueError, or unpickling exceptions. If any
                # of these happen, reset the session.
                self.create()
        return {}
