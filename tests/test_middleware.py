from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings


class RotateAuthenticationMiddlewareTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.password = '124#12@!'
        self.u = User.objects.create_user(username='asdas', password=self.password)

    def test_login_required(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)  # it redirects us to login page

        self.client.post('/login', {'username': self.u.username, 'password': self.password})

        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)  # now we are logged in

    def test_session_breaks(self):
        self.client.post('/login', {'username': self.u.username, 'password': self.password})

        with self.settings(SECRET_KEY='newsecretkey'):
            response = self.client.get('/profile')
            # BROKEN! because secret_key has changed
            self.assertNotEqual(response.status_code, 200)

    def test_support_old_key(self):
        self.client.post('/login', {'username': self.u.username, 'password': self.password})
        old_key = settings.SECRET_KEY

        with self.settings(SECRET_KEY='newsecretkey', OLD_SECRET_KEY=old_key):
            response = self.client.get('/profile')
            # Still logged in, thanks to OLD_SECRET_KEY support, even after secret key change
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.u.username)

            # Remove support for old key, STILL logged in, and to this own account
            with self.settings(OLD_SECRET_KEY=None):
                response = self.client.get('/profile')
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, self.u.username)
