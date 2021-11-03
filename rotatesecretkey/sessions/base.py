import logging

import django
from django.contrib.sessions.backends.base import SessionBase, salted_hmac
from django.conf import settings
from django.core import signing


class RotateSecretKeyMixIn(SessionBase):
    def __init__(self, *args, **kwargs):
        self.try_old_key = False
        super().__init__(*args, **kwargs)

    def _hash(self, value):
        key_salt = "django.contrib.sessions" + self.__class__.__name__
        secret = (
            getattr(settings, 'OLD_SECRET_KEY', None)
            if self.try_old_key
            else None
        )
        # clear the try_old_key bit for future tries
        self.try_old_key = False
        return salted_hmac(key_salt, value, secret=secret).hexdigest()

    def inner_decode(self, session_data):
        if django.VERSION < (3, 0):
            # Django 2.2 path.
            return super().decode(session_data)
        # Supply the old secret key if needed
        key = (
            getattr(settings, 'OLD_SECRET_KEY', None)
            if self.try_old_key
            else None
        )
        try:
            return signing.loads(
                session_data,
                key=key,
                salt=self.key_salt,
                serializer=self.serializer,
            )
        # RemovedInDjango40Warning: when the deprecation ends, handle here
        # exceptions similar to what _legacy_decode() does now.
        except signing.BadSignature:
            try:
                # Return an empty session if data is not in the pre-Django 3.1
                # format.
                return self._legacy_decode(session_data)
            except Exception:
                logger = logging.getLogger(
                    'django.security.SuspiciousSession')
                logger.warning('Session data corrupted')
                return {}
        except Exception:
            return self._legacy_decode(session_data)

    def decode(self, session_data):
        decoded_session = self.inner_decode(session_data)
        # new key failed at decoding try once more with old key
        if decoded_session == {}:
            self.try_old_key = True
            decoded_session = self.inner_decode(session_data)
        return decoded_session
