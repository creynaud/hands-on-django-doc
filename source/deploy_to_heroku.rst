Deploying the notes web app
===========================

How is this going to work?
--------------------------

Here is how our notes web app will run on Heroku:

* We are going to push our web app git local repository to a remote heroku origin
* After the push, Heroku will download our app requirements, build the app and create a "slug". A "slug" is a snapshot of our app that can be easily deployed on a Heroku "dyno". A Heroku "dyno" can be seen as a small Virtual Machine with an ephemeral file system. To scale the app up or down, one can add/remove "dynos".
* An instance of the note app that runs on a "dyno" is stateless. Sessions are tracked in the database, not inside the "dyno" itself.
* The Postgresql database can be provided by Heroku via an add-on: https://addons.heroku.com/
* Heroku expects that the web app configuration is defined as environment variables. For example, when one adds a postgresql add-on to a Heroku app, a DATABASE_URL variable is added to the environment of the app.
* We will tell Heroku to run our app on gunicorn (http://gunicorn.org/), a python WSGI HTTP server, by creating a Procfile.
* Our app static files (e.g theme.css) will also be served by the "dynos", thank to dj-static (https://github.com/kennethreitz/dj-static). Note that another option could be to serve the static files via Amazon S3 (http://aws.amazon.com/en/s3/), but we won't do it during this workshop for the sake of simplicity.

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

We are going to modify our settings.py file to get its values from these environment variables (also install dj-database-url):

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

Also let's declare a static root in settings.py:

.. code-block:: python
    :emphasize-lines: 4

     # Static files (CSS, JavaScript, Images)
     # https://docs.djangoproject.com/en/1.6/howto/static-files/

    +STATIC_ROOT = 'staticfiles'
     STATIC_URL = '/static/'

The static root is the folder where all the project static files are going to be copied when calling 'collectstatic'.
See https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/ for the documentation of how collectstatic finds the static files.

Listing the requirements of the project for deployment
------------------------------------------------------

To get a list of the requirements of the project, call pip freeze:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip freeze
    Django==1.6.2
    WebOb==1.3.1
    .......
    waitress==0.8.8
    wsgiref==0.1.2

Some of these requirements are only needed for development, so let's split the requirements in 2 lists: one for development, and one for deployment.
The following requirements should go in a requirements.txt file at the root of your project:

.. code-block:: python

    Django==1.6.2
    argparse==1.2.1
    dj-database-url==0.2.2
    dj-static==0.0.5
    django-allauth==0.15.0
    django-bootstrap3==2.5.6
    gunicorn==18.0
    oauthlib==0.6.1
    psycopg2==2.5.2
    pystache==0.5.3
    python-openid==2.2.5
    requests==2.2.1
    requests-oauthlib==0.4.0
    six==1.5.2
    sqlparse==0.1.11
    static==1.0.2
    wsgiref==0.1.2

Always put *all* your project requirements (even dependencies of requirements) in this file. Also always specify an exact version.
You can have some bad surprises when checking out your project on another machine and some version gets updated silently.

The following requirements should go in a requirements-dev.txt file:

.. code-block:: python

    -r requirements.txt
    WebOb==1.3.1
    WebTest==2.0.14
    argparse==1.2.1
    beautifulsoup4==4.3.2
    django-debug-toolbar==1.0.1
    django-webtest==1.7.6
    factory-boy==2.3.1
    waitress==0.8.8

Note: if you checkout the project on another machine, you can install all the requirements like this:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip install -r requirements-dev.txt

Finally you should tell Heroku which version of python to use via a runtime.txt file at the root of your project:

.. code-block:: python

    python-2.7.5

Prepare the notes web app on Heroku
-----------------------------------

Sign-up to Heroku.

Generate an ssh key and add it to your Heroku account:

.. code-block:: bash

    pony@Pony-VirtualBox:~$ ssh-keygen -t rsa

Add the public key (~/.ssh/id_rsa.pub) to your Heroku account.

Create an app (either in the US or Europe), and also add the Heroku postgres add-on to the app.

Add heroku origin, and push your local repository to heroku:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ git remote add heroku git@heroku.com:notes-last-test.git

Have a look at your Heroku app environment variables (you will have to enter your Heroku credentials):

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku config
    Authentication failure
    Enter your Heroku credentials.
    Email: pinky@acme.com
    Password (typing will be hidden):
    Authentication successful.
    === notes-last-test Config Vars
    HEROKU_POSTGRESQL_PINK_URL: postgres://somekey.amazonaws.com:5432/someotherkey
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

So far only the database URL is defined. Let's add the other environment variables.

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku config:set SECRET_KEY='some-random-key'
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku config:set ALLOWED_HOSTS='yourapp.herokuapp.com'
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku config:set DJANGO_SETTINGS_MODULE='notes.settings'

No need to set the DEBUG variable, not specifying it defaults to False.

There is one last thing we need to do before deploying. We need to tell Heroku to use our environment variables while building the app slug (https://devcenter.heroku.com/articles/labs-user-env-compile):

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku labs:enable user-env-compile
    Enabling user-env-compile for notes-last-test... done
    WARNING: This feature is experimental and may change or be removed without notice.
    For more information see: http://devcenter.heroku.com/articles/labs-user-env-compile
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

Let's push our local git repository to heroku remote
----------------------------------------------------

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ git push heroku master
    Initializing repository, done.
    Counting objects: 124, done.
    Compressing objects: 100% (105/105), done.
    Writing objects: 100% (124/124), 15.81 KiB | 0 bytes/s, done.
    Total 124 (delta 49), reused 0 (delta 0)

    -----> Python app detected
    -----> Preparing Python runtime (python-2.7.5)
    -----> Installing Distribute (0.6.36)
    -----> Installing Pip (1.3.1)
    -----> Installing dependencies using Pip (1.3.1)
           Downloading/unpacking Django==1.6.2 (from -r requirements.txt (line 1))
    ....
    -----> Collecting static files
       70 static files copied to '/app/staticfiles'.

    -----> Discovering process types
           Procfile declares types -> web

    -----> Compressing... done, 34.3MB
    -----> Launching... done, v8
           http://yourapp.herokuapp.com deployed to Heroku

Now you can open http://yourapp.herokuapp.com in a browser.

You will get an internal server error (500) if you try to login, because the far the database does not contain any of the app tables.
Let's call syncdb:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ heroku run python manage.py syncdb
    Running `python manage.py syncdb` attached to terminal... up, run.9823
    Creating tables ...
    Creating table django_admin_log
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_groups
    Creating table auth_user_user_permissions
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table notesapp_note
    Creating table account_emailaddress
    Creating table account_emailconfirmation
    Creating table socialaccount_socialapp_sites
    Creating table socialaccount_socialapp
    Creating table socialaccount_socialaccount
    Creating table socialaccount_socialtoken

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'u20149'): someadminname
    Email address: someadminname@acme.com
    Password:
    Password (again):
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

Try to login again with your admin credentials. This time it should work.

If you try to sign-up with another user, call 'heroku logs' to click on the activation link (no SMTP server is set up so far).

If the static files are not served, have a look at the deploy console logs and look for "Collecting static files". This should be done while Heroku builds the app slug.
Verify your settings.py static configuration and that you called 'heroku labs:enable user-env-compile'.
