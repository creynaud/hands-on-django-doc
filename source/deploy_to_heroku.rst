Deploying the notes web app
===========================

Make the notes web app deployable
---------------------------------

There is a comment in settings.py mentioning that the settings generated when starting a Django project are 'Quick-start development settings - unsuitable for production'.
The comment also points to https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/.
Looks like a good place to get started.

See also this Heroku documentation about deploying a Django app on Heroku: https://devcenter.heroku.com/articles/getting-started-with-django.

Deploy the notes web app to Heroku
----------------------------------

Sign-up to Heroku.

Generate an ssh key and add it to your Heroku account:

.. code-block:: bash

    pony@Pony-VirtualBox:~$ ssh-keygen -t rsa

Add the public key (~/.ssh/id_rsa.pub) to your Heroku account.

Create an app (either in the US or Europe), and also add the Heroku postgres add-on to the app.

