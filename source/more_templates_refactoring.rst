More templates refactoring
==========================

In this step we are going to make our views look "nicer", and also make them display a content more similar to our target app (http://django-notes.herokuapp.com/).

There are several things we will do:

* Use bootstrap, to have a nicer look
* Start to use static files, because we will write a few lines of CSS for our website
* Refactor our notes views to always show the list of notes

Using bootstrap in base.html
----------------------------

Bootstrap (http://getbootstrap.com/) is a popular framework that helps you "bootstrap" a web front-end, by providing some CSS, javascript and fonts.
With Bootstrap you can easily implement responsive websites that will show up nicely on mobile devices.

We are also going to use django-bootstrap3, which is a helper package:

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip install django-bootstrap3

Let's update our settings.py:

.. code-block:: python

     INSTALLED_APPS = (
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.sites',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'notesapp',
         'allauth',
         'allauth.account',
         'allauth.socialaccount',
    +    'bootstrap3',
     )

    +STATICFILES_DIRS = (
    +    os.path.join(BASE_DIR, 'notes/static'),
    +)

Here is our new base.html template that uses bootstrap (it is more or less this bootstrap example: http://getbootstrap.com/examples/starter-template/):

.. code-block:: html

    {% load staticfiles bootstrap3 %}

    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>{% block head_title %}Notes{% endblock %}</title>

        {% bootstrap_css %}
        <link href="{% static 'notes/css/theme.css' %}" rel="stylesheet">
    </head>
    <body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="{% url 'home' %}">Notes</a>
            </div>
            <div class="collapse navbar-collapse">
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="{% url 'home' %}">Home</a></li>
                    {% if user.is_authenticated %}
                        <li><a href="{% url 'my_notes' %}">My Notes</a></li>
                        <li><a href="{% url 'account_logout' %}">Logout</a></li>
                    {% else %}
                        <li><a href="{% url 'account_login' %}">Login</a></li>
                    {% endif %}
                </ul>
            </div>
            <!--/.nav-collapse -->
        </div>
    </div>
    <div class="container container-top-padding">
        {% bootstrap_messages %}
        {% block content %}{% endblock %}
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    {% bootstrap_javascript %}
    </body>
    </html>

Create a css file: notes/static/notes/css/theme.css (notes/static is the folder we set in STATICFILES_DIRS in settings.py)

.. code-block:: css

    .container-top-padding {
        padding-top: 50px;
    }

    #messages {
        padding-top: 10px;
    }

Refactor the notes views to always show the list of notes
---------------------------------------------------------

We want to show the notes list in all the notes views now. So let's create the following mixin in notesapp/views.py

.. code-block:: python

    class UserNotesInContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserNotesInContextMixin, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(owner=self.request.user)
        return context

Make all the notes view classes inherit from this mixin 1st, e.g:

.. code-block:: python

    class MyNotes(UserNotesInContextMixin, ListView):
        ....

Now we can modify the notes view templates. All the notes views should show the list of notes, so let's add an intermediate parent template.
Let's add a notesapp/templates/notesapp/base.html, that shows the notes list on the left ({% block content_left %}), and something else on the right ({% block content_right %}).
Note the col-md-3 and col-md-9 css classes. These are bootstrap classes that say the left content takes 3 columns and the right content takes 9 columns (there are 12 columns total).

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        <div class="row">
            <div class="col-md-3">
                {% block content_left %}
                    <h1>
                        My Notes
                        <a href=""><span class="glyphicon glyphicon-plus"></span></a>
                    </h1>
                    {% if notes %}
                        <ul>
                            {% for note in notes %}
                                <li><a href="{% url 'note_detail' note.id %}">{{ note.title }}</a></li>
                            {% endfor %}
                        </ul>
                    {% else %}
                        <p>You don't have any note yet.</p>
                    {% endif %}
                {% endblock %}
            </div>
            <div class="col-md-9">
                {% block content_right %}{% endblock %}
            </div>
        </div>
    {% endblock %}

Now the note edition template will look like this:

.. code-block:: html

    {% extends "notesapp/base.html" %}

    {% load bootstrap3 %}

    {% block head_title %}Edit Note{% endblock %}

    {% block content_right %}
        <h1>Edit note '{{ note.title }}'</h1>

        <form method="post" id="edit-note-form">
            {% csrf_token %}
            {% bootstrap_form form %}
            {% buttons %}
                <input type="submit" value="Update" class="btn btn-primary">
                <a href="{% url 'note_detail' note.id %}" class="btn btn-default">Cancel</a>
            {% endbuttons %}
        </form>
    {% endblock %}

Finally modify the last templates: my_notes.html and note_detail.html. Let's just display the 1st note detail on the right side in the notes view (we don't want to show the notes list twice).

Don’t forget to commit your changes before going to the next step.
