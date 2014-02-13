Create the Notes Django project
===============================

.. code-block:: python

    pony@Pony-VirtualBox:~$ mkdir hands-on-django
    pony@Pony-VirtualBox:~$ cd hands-on-django

Create a virtualenv for the new project. This is were all the project dependencies will reside, without polluting or conflicting with the system libraries.

.. code-block:: python

    pony@Pony-VirtualBox:~/hands-on-django$ mkvirtualenv --python=python2.7 hands-on-django
    Running virtualenv with interpreter /usr/bin/python2.7
    New python executable in hands-on-django/bin/python2.7
    Also creating executable in hands-on-django/bin/python
    Installing Setuptools..............................................................................................................................................................................................................................done.
    Installing Pip.....................................................................................................................................................................................................................................................................................................................................done.
    virtualenvwrapper.user_scripts creating /home/pony/.virtualenvs/hands-on-django/bin/predeactivate
    virtualenvwrapper.user_scripts creating /home/pony/.virtualenvs/hands-on-django/bin/postdeactivate
    virtualenvwrapper.user_scripts creating /home/pony/.virtualenvs/hands-on-django/bin/preactivate
    virtualenvwrapper.user_scripts creating /home/pony/.virtualenvs/hands-on-django/bin/postactivate
    virtualenvwrapper.user_scripts creating /home/pony/.virtualenvs/hands-on-django/bin/get_env_details
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

Install Django:

.. code-block:: python

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip install Django
    Downloading/unpacking Django
      Downloading Django-1.6.2.tar.gz (6.6MB): 6.6MB downloaded
      Running setup.py egg_info for package Django
    ...
    Successfully installed Django
    Cleaning up...
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

Create the notes Django project by calling django-admin.py:

.. code-block:: python

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ django-admin.py help
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ django-admin.py startproject notes .
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ ls -lR
    .:
    total 8
    -rw-r--r-- 1 pony pony  248 févr. 13 14:30 manage.py
    drwxr-xr-x 2 pony pony 4096 févr. 13 14:30 notes

    ./notes:
    total 12
    -rw-r--r-- 1 pony pony    0 févr. 13 14:30 __init__.py
    -rw-r--r-- 1 pony pony 1969 févr. 13 14:30 settings.py
    -rw-r--r-- 1 pony pony  296 févr. 13 14:30 urls.py
    -rw-r--r-- 1 pony pony  385 févr. 13 14:30 wsgi.py
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django

Open the project in Pycharm: File->Open... Then select the path to the hands-on-django directory.
Open the project settings, File->Settings... and search "python intrepreters". Add the path to your 'hands-on-django' virtualenv python, which should be /home/pony/virtualenvs/hands-on-django/bin/python.
Finally accept to use this python interpreter for the current project.

Pycharm will re-build its indexes.

Try to run the project, either in Pycharm or via the command line:

.. code-block:: python

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ python manage.py runserver
    Validating models...

    0 errors found
    February 13, 2014 - 13:56:43
    Django version 1.6.2, using settings 'notes.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Open http://127.0.0.1:8000/ in Firefox or Chrome. You should see a page saying "It worked!".

Let's have a look at all the files that were created when starting the new Django project.

Before going to the next step, save your work in git.

.. code-block:: python

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ git init
    Initialized empty Git repository in /home/pony/hands-on-django/.git/

Commit all files except the .idea and *.pyc which should go in the .gitignore
