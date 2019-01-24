from django.core import signing
from django.conf import settings


class RotateSigner(signing.Signer):
    def __init__(self, key=None, accept_old=True, **kwargs):
        self.key = key or settings.SECRET_KEY
        self.old_key = None
        if accept_old:
            self.old_key = getattr(settings, 'OLD_SECRET_KEY', None)
        super().__init__(**kwargs)

    def unsign(self, signed_value):
        try:
            return super().unsign(signed_value)
        except signing.BadSignature:
            temp_key = self.key
            self.key = self.old_key
            try:
                return super().unsign(signed_value)
            except signing.BadSignature:
                print('OLD KEY FAILED AS WELL')
                self.key = temp_key
                raise signing.BadSignature()