Templates refactoring: base template and links between pages
============================================================

It's very likely that your html templates will have some common parts. For example, pages on a website usually have the same header and footer.
Let's start refactoring our templates to use a common template as the base.

Let's add a base.html template in notes/templates. Naming the root template base.html is a convention.

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block head_title %}Notes{% endblock %}</title>
    </head>
    <body>
    <a href="{% url "home" %}">Home</a>
    {% if user.is_authenticated %}
        <a href="{% url "my_notes" %}">My Notes</a>
        <a href="{% url "account_logout" %}">Logout</a>
    {% else %}
        <a href="{% url "account_login" %}">Login</a>
    {% endif %}

    {% block content %}{% endblock %}
    </body>
    </html>

Unlike the other templates, we don't put base.html in notes/templates/notes or notesapp/templates/notesapp, because we want other apps templates to inherit from base.html.
Have a look at the templates from django-allauth. You will see that they inherit from a base.html template.

Also note that the new base.html template contains links to other pages: my notes, login or logout page.

Now let's refactor our views to extend this base template. Here is the new version of notes/index.html:

.. code-block:: html

    {% extends "base.html" %}

    {% block head_title %}Notes{% endblock %}

    {% block content %}
        <h1>Welcome{% if user.is_authenticated %} {{ user.email }}{% endif %}!</h1>

        <p>This is the Notes App. Django powered!</p>

        <p>{{ date }}</p>
    {% endblock %}

Now you can update all the other templates in notes and notesapp to make them extend base.html.
When relevant, also add links between the pages. For example, the notes list should link to note detail views.
You can have a look at the Django documentation for templates https://docs.djangoproject.com/en/dev/topics/templates/, and especially the "Template inheritance" paragraph.
