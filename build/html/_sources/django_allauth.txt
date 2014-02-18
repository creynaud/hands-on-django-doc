Authentication with django allauth
==================================

Django allauth let's you implement local or social authentication for your Django website.
It provides views that will typically reside under /accounts, e.g /accounts/login/, /accounts/logout. Follow the installation guide: http://django-allauth.readthedocs.org/en/latest/.

For the settings which are not yet in your settings.py, look at the default values in Django's settings reference documentation: https://docs.djangoproject.com/en/dev/ref/settings/.

You will also need an email backend, so add the following setting too:

.. code-block:: python

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

This will log the allauth emails (for email verification, reset password...) to the console.

It would be nice to:

* be redirected to the 'my notes' page after logging in (instead of /accounts/profile/)
* require the user to enter an email on signup
* make email verification mandatory

You can also add a tool that can be helpful when debugging: the Django Debug Toolbar.

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip install django-debug-toolbar

Also add the following code in your project's settings.py

.. code-block:: python

    if DEBUG:
        INSTALLED_APPS += (
            'debug_toolbar',
        )

Refresh http://127.0.0.1:8000/, you should now see the debug toolbar on the right hand side. Click on templates or SQL for example to see which debug information it can provide.

Don’t forget to commit your changes before going to the next step.
