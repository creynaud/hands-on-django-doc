Deploying the notes web app
===========================

How is this going to work?
--------------------------

Here is how our app will run on Heroku:

* We are going to push our web app git local repository to a remote heroku origin
* After the push, Heroku will download our app requirements, build the app and create a "slug". A "slug" is a snapshot of our app that can be easily deployed on a Heroku "dyno". A Heroku "dyno" can be seen as a small Virtual Machine with an ephemeral file system. To scale the app up or down, one can add/remove "dynos".
* An instance of the note app that runs on a "dyno" is stateless. Sessions are tracked in the database, not inside the "dyno" itself.
* The Postgresql database can be provided by Heroku via an add-on: https://addons.heroku.com/
* Heroku expects that the web app configuration is defined as environment variables. For example, when one adds a postgresql add-on to an Heroku app, a DATABASE_URL variable is added to the environment of the app.
* We will tell Heroku to run our app on gunicorn, a wsgi server, by creating a Procfile.
* Our app static files (e.g theme.css) will also be served by the "dynos", thank to dj-static. Note that we could serve the static files via Amazon S3 (http://aws.amazon.com/en/s3/), but we won't do it during this workshop for the sake of simplicity.

Some documentation pointers to get started
------------------------------------------

There is a comment in settings.py mentioning that the settings generated when starting a Django project are 'Quick-start development settings - unsuitable for production'.
The comment also points to https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/.
Looks like a good place to get started.

See also this Heroku documentation about deploying a Django app on Heroku: https://devcenter.heroku.com/articles/getting-started-with-django.

Defining the notes app configuration as environment variables
-------------------------------------------------------------

As Heroku expects the configuration to be defined as environment variables, let's define the following variables:

* DATABASE_URL
* DEBUG
* ALLOWED_HOSTS
* SECRET_KEY
* DJANGO_SETTINGS_MODULE

We are going to modify our settings.py file to get its values from these environment variables:

.. code-block:: python
    :emphasize-lines: 12, 16, 19, 22, 32

     # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
     import os
    +import dj_database_url

     from django.core.urlresolvers import reverse_lazy

     BASE_DIR = os.path.dirname(os.path.dirname(__file__))

     # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
     # SECURITY WARNING: keep the secret key used in production secret!
    -SECRET_KEY = 'dummy'
    +SECRET_KEY = os.environ['SECRET_KEY']

     # SECURITY WARNING: don't run with debug turned on in production!
    -DEBUG = True
    +DEBUG = bool(os.environ.get('DEBUG', False))

    -TEMPLATE_DEBUG = True
    +TEMPLATE_DEBUG = DEBUG

    -ALLOWED_HOSTS = []
    +ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()

     # Application definition
     # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

     DATABASES = {
    -    'default': {
    -        'ENGINE': 'django.db.backends.sqlite3',
    -        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    -    }
    +    'default': dj_database_url.config()
     }

Now if you try to launch the app for development, it should be broken unless you define the right environment variables:

* DATABASE_URL='sqlite:////home/pony/hands-on-django/db.sqlite3'
* SECRET_KEY='dummy'
* ALLOWED_HOSTS='dummy'
* DJANGO_SETTINGS_MODULE='notes.settings'
* DEBUG='True'

To run your project and tests in Pycharm, add these variables in the run configuration settings.

If you run your project from the command line (which is quite likely if you use an integration server), you can use a tool called 'envdir'.
'envdir' is command line tool that accepts a folder containing files defining environment variable as parameter.

For example, create an 'env' folder at the root of the project. Define a DATABASE_URL file that just contains its value: sqlite:////home/pony/hands-on-django/db.sqlite3 as value.
Do the same for the other environment variable. Now to run your project or your tests from the command line, just call:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ envdir env/ python manage.py runserver
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ envdir env/ python manage.py test

Telling Heroku to run the notes app with gunicorn
-------------------------------------------------

Create a Procfile at the root of the project. The Procfile content should be the following:

.. code-block:: python

    web: gunicorn notes.wsgi

We need gunicorn, so let's install it via pip.

Serving static files via Heroku and dj-static
---------------------------------------------

We are going to serve our notes app static files (theme.css and all admin app static files - images, css, javascript files) via Heroku.
This is possible thank to the dj-static package.

We need to install dj-static and static for this purpose.

We also need to change the notes.wsgi file to the following:

.. code-block:: python
    :emphasize-lines: 2, 7, 8

     import os
    +
     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notes.settings")

     from django.core.wsgi import get_wsgi_application
    -application = get_wsgi_application()
    +from dj_static import Cling
    +application = Cling(get_wsgi_application())

Listing the requirements of the project for deployment
------------------------------------------------------

To get a list of the requirements of the project,

Prepare the notes web app on Heroku
-----------------------------------

Sign-up to Heroku.

Generate an ssh key and add it to your Heroku account:

.. code-block:: bash

    pony@Pony-VirtualBox:~$ ssh-keygen -t rsa

Add the public key (~/.ssh/id_rsa.pub) to your Heroku account.

Create an app (either in the US or Europe), and also add the Heroku postgres add-on to the app.

Make the notes web app deployable
---------------------------------

