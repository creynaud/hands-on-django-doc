Fixing some security issues
===========================

Check your pony
---------------

http://ponycheckup.com/

Note from ponycheckup: "This is not a replacement for a full security audit."

Let's modify the settings.py
----------------------------

If you read Django's deployment checklist (https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/), you should have read the https recommendations.
Add the following to your settings.py if this is not already done:

.. code-block:: python

    if not DEBUG:
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

This way session and csrf cookies will never be transmitted over http. But our website still does not force https.

Let's install django-secure (https://pypi.python.org/pypi/django-secure). Don't forget to add it in requirements.txt too.
Read the doc and modify your settings.py accordingly.

Re-deploy to Heroku and check that trying to access your app via http redirects to https.
