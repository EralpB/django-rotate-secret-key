================================
Django Rotate Secret Key
================================

Helps rotating your secret keys safely without losing user sessions, which means without logging users out.

Compatible with modern Django versions. At the moment of writing that's including 1.11 and 2.0 on Python 3.7.

I haven't found any library to allow us to do this on our production website, so I started the library.

Problem
============
Once you change the ``SECRET_KEY`` on production, all the old sessions and cookies are invalidated,
users are logged out and data in sessions are lost.

This is good if your ``SECRET_KEY`` is compromised!
But not good if you just want to rotate in a regular schedule for security purposes.

This library allows you to continue supporting old sessions signed with your old secret key,
while rewriting them with the new secret key if the user comes to the website.

So optimal schedule would be

- you decide to rotate your secret key
- Install ``django-rotate-secret-key`` and configure
- Support both keys for a limited time (x months)
- Roll back ``django-rotate-secret-key`` and keep your secret key the same (removing the old one)

If a user comes back to the website after x months, his session will be invalidated.
But for all the regular users this should be seamless transition.

Compatibility
=============

If you are using JWT tokens created by ``django-rest-framework-jwt``, currently package is not compatible. But it will
be supported in version 1.0.

Getting It
============
::

    $ pip install django-rotate-secret-key

Installing It
==============

This is safe to do even before you decide to rotate your keys,
it basically has no effect before you change the settings.::

    INSTALLED_APPS = (
        ...
        'rotatesecretkey',
        ...
    )

Settings
============

Replace AuthenticationMiddleware with RotateAuthenticationMiddleware::

    MIDDLEWARE = [
        ...
        # 'django.contrib.auth.middleware.AuthenticationMiddleware',
        'rotatesecretkey.middleware.RotateAuthenticationMiddleware',
        ...
    ]

Replace SESSION_ENGINE::

    SESSION_ENGINE = 'rotatesecretkey.sessions'

Add the old secret key into OLD_SECRET_KEY, and create a new ``SECRET_KEY``.::

    SECRET_KEY = 'NEWRANDOMKEY'
    OLD_SECRET_KEY = 'your_previous_secret_key_that_you_want_to_support'

Once these changes go live your website will decode old sessions with
the OLD_SECRET_KEY and resign them with the new ``SECRET_KEY``.

After some time (like 1 or 2 months) you should roll these changes back and just keep the ``SECRET_KEY``.::

    SECRET_KEY = 'NEWRANDOMKEY'

You don't want to support ``OLD_SECRET_KEY`` forever but long enough to give your visitors a
chance to visit the website and rewrite their sessions with the new key.