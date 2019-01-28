# this class is not required for supporting old sessions
# if you use the Signer yourself in the project you need to patch it as well
# from django.core import signing
# from django.conf import settings
#
#
# class RotateSigner(signing.Signer):
#     def __init__(self, key=None, accept_old=True, **kwargs):
#         self.key = key or settings.SECRET_KEY
#         self.old_key = None
#         if accept_old:
#             self.old_key = getattr(settings, 'OLD_SECRET_KEY', None)
#         super().__init__(**kwargs)
#
#     def unsign(self, signed_value):
#         try:
#             return super().unsign(signed_value)
#         except signing.BadSignature:
#             temp_key = self.key
#             self.key = self.old_key
#             try:
#                 return super().unsign(signed_value)
#             except signing.BadSignature:
#                 self.key = temp_key
#                 raise signing.BadSignature()
#
# and the tests
#
# from mock import Mock
# from django.test import TestCase
# from rotatesecretkey.signing import RotateSigner
# from django.test.utils import override_settings
#
#
# class RotateSignerTests(TestCase):
#
#     def setUp(self):
#         self.base_rs = RotateSigner(accept_old=False)
#         self.new_rs = RotateSigner()
#         self.random_text = '150ds0m1@3122kmas'
#
#     def test_basecase(self):
#         signed_value = self.base_rs.sign(self.random_text)
#
#         self.assertEqual(
#             self.base_rs.unsign(signed_value),
#             self.random_text)
#
#     def test_newcase(self):
#         signed_value = self.new_rs.sign(self.random_text)
#
#         self.assertEqual(
#             self.new_rs.unsign(signed_value),
#             self.random_text)
#
#     @override_settings(OLD_SECRET_KEY='thisdoesntmatterforthis')
#     def test_newcase_with_old_key_setting(self):
#         signed_value = self.new_rs.sign(self.random_text)
#
#         self.assertEqual(
#             self.new_rs.unsign(signed_value),
#             self.random_text)