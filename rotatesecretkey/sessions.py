from django.contrib.sessions.backends.base import SessionBase, salted_hmac
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore as BaseSessionStore


class SessionStore(BaseSessionStore):
    def __init__(self, *args, **kwargs):
        self.try_old_key = False
        super().__init__(*args, **kwargs)

    def _hash(self, value):
        key_salt = "django.contrib.sessions" + self.__class__.__name__
        secret = getattr(settings, 'OLD_SECRET_KEY', None) if self.try_old_key else None
        # clear the try_old_key bit for future tries
        self.try_old_key = False
        return salted_hmac(key_salt, value, secret=secret).hexdigest()

    def decode(self, session_data):
        decoded_session = super().decode(session_data)
        # new key failed at decoding try once more with old key
        if decoded_session == {}:
            self.try_old_key = True
            return super().decode(session_data)
        else:
            return decoded_session
