Notes App
=========

Django projects vs. Django apps
-------------------------------

From Django documentation:
"What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a particular Web site. A project can contain multiple apps. An app can be in multiple projects."

An app is a reusable component that can be used by several websites. Several websites could use a notes component, so let's create an app.

Creating the notes app
----------------------

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ python manage.py startapp notesapp

The notesapp is a python package, which contains 3 files:

* models.py: will contain the definition of the note entities. These will be mapped to the database via Django ORM.
* admin.py: will contain the registration of the model entities so they can show up in the admin.
* views.py: will contain the app views (e.g notes detail view, notes edition view, notes list view...)
Also create a urls.py file inside notesapp/. It can be left empty so far.

Plugging the notes app in the project
-------------------------------------

First let's declare our app in the project settings:

.. code-block:: python
    :emphasize-lines: 8

     INSTALLED_APPS = (
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
    +    'notesapp',
     )

Also let's plug the notes app urls in the project root urls:

.. code-block:: python
    :emphasize-lines: 6,7

     urlpatterns = patterns(
         '',

         url(r'^$', 'notes.views.home', name='home'),
         # url(r'^blog/', include('blog.urls')),
    -
    +    url(r'^notes/', include('notesapp.urls')),
         url(r'^admin/', include(admin.site.urls)),
     )

This way the urls from the notes app will reside under http://127.0.0.1:8000/notes/.

Implementing the notes view
---------------------------

The notes view should display all the note titles.

So far we just want to render a static template when someone accesses http://127.0.0.1:8000/notes/.
The template should go in a notesapp/templates/notesapp/notes.html. Again, the notesapp folder under templates allows to have some namespacing for the template files.

Just follow the same steps as for the home view, except that now you should only modify files inside notesapp/.
Verify that the new view shows up in your browser.

Now it is time to add a model for the notes. Add the following code in notesapp/models.py:

.. code-block:: python

    from django.contrib.auth.models import User
    from django.db import models


    # Create your models here.
    from django.utils import timezone


    class Note(models.Model):
        title = models.CharField(max_length=256)
        content = models.TextField(blank=True)
        creation_date = models.DateTimeField(default=timezone.now)
        owner = models.ForeignKey(User)

You can have a look at the Django documentation for model fields if you want more details on the field types: https://docs.djangoproject.com/en/1.6/ref/models/fields/.

In order to use this model, we need to create the corresponding tables in our database.

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ python manage.py syncdb
    Creating tables ...
    Creating table notesapp_note
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)
    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$

Now let's add the actual current user notes in the 'notes' view.

.. code-block:: python
    :emphasize-lines: 1

    +    context = RequestContext(request, {'notes': Note.objects.all()})

The Note.objects.all() is a call to the Django ORM (https://docs.djangoproject.com/en/1.6/topics/db/queries/) and retrieves all the notes.

We also need to update the template to actually show the notes:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Notes</title>
    </head>
    <body>
    <ul>
    {% for note in notes %}
        <li>{{ note.title }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>

Refresh http://127.0.0.1:8000/notes. Maybe you don't have any notes so far. To be able to add a Note, let's register the Note model in notesapp/admin.py:

.. code-block:: python

    from django.contrib import admin

    # Register your models here.
    from .models import Note

    admin.site.register(Note)

Testing
-------

Let's write a test for this new view. Take the previous tests as example.

Don’t forget to commit your changes before going to the next step.

