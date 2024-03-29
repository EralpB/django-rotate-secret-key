================================
Django Rotate Secret Key
================================

Helps rotating your secret keys safely without losing user sessions, which means without logging users out.

Compatible with Django versions 2.2, 3.1 and 3.2.

I haven't found any library to allow us to do this on our production website, so I started the library.

Medium Post
============
https://medium.com/@bayraktar.eralp/changing-rotating-django-secret-key-without-logging-users-out-804a29d3ea65?sk=6fe95fa587574e5875b630617f3ecc91

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

If you are using JWT tokens created by ``django-rest-framework-jwt``, currently package is not compatible.

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

Things to keep in mind
======================

This library allows keeping Sessions intact and allowing seamless transition for your visitors, if you are using
Django's signing features manually for other purposes (like signing your backups etc.) a generic library cannot take it
into account.

What SECRET_KEY doesn't break
=============================

Even if you don't use this library SECRET_KEY is not used to encrypt user password or OAUTH tokens. So you shouldn't
worry about them during your key rotation.
