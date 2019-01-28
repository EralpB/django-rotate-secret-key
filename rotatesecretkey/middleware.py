from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import settings
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import _get_user_session_key, BACKEND_SESSION_KEY, load_backend, HASH_SESSION_KEY
from django.utils.crypto import constant_time_compare, salted_hmac


def get_user(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from django.contrib.auth.models import AnonymousUser
    user = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if hasattr(user, 'get_session_auth_hash'):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
                    session_hash_verified = session_hash and constant_time_compare(
                        session_hash,
                        salted_hmac(key_salt, user.password, secret=settings.OLD_SECRET_KEY).hexdigest()
                    )

                    request.session.cycle_key()
                    request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()

                if not session_hash_verified:
                    request.session.flush()
                    user = None

    return user or AnonymousUser()


def cached_get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = get_user(request)
    return request._cached_user


class RotateAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: cached_get_user(request))