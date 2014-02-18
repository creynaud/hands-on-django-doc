Let's implement a note detail view
==================================

Let's implement a note detail view. You should use a class based view: DetailView, from django.views.generic.detail (https://docs.djangoproject.com/en/dev/ref/class-based-views/generic-display/).

The view path should be http://127.0.0.1:8000/notes/1/ for a note with id=1.
Here is the regular expression that you will use in notesapp/urls.py:

.. code-block:: python

    url(r'^(?P<pk>\d+)/$', views.note_detail, name='note_detail'),

Let's add tests for this view too.

When you are done with the tests, you may notice that you repeat User and Note objects creation quite a lot.
Let's improve this and refactor the tests with Factory Boy (https://factoryboy.readthedocs.org/en/latest/introduction.html).

.. code-block:: bash

    (hands-on-django)pony@Pony-VirtualBox:~/hands-on-django$ pip install factory_boy

Factory Boy let's you instantiate your models via factories, without having to specify all the instance values.

Create a tests/factories.py file, and paste the following content:

.. code-block:: python

    from django.contrib.auth.models import User

    from factory.declarations import Sequence, SubFactory
    from factory.django import DjangoModelFactory
    from factory.helpers import lazy_attribute

    from notesapp.models import Note


    class UserFactory(DjangoModelFactory):
        FACTORY_FOR = User
        username = Sequence(lambda n: 'some_email{0}@acme.com'.format(n))

        @lazy_attribute
        def email(self):
            return self.username

        @lazy_attribute
        def password(self):
            return "123"


    class NoteFactory(DjangoModelFactory):
        FACTORY_FOR = Note
        owner = SubFactory(UserFactory)

        @lazy_attribute
        def title(self):
            return "Some Title"

        @lazy_attribute
        def content(self):
            return "Some content."

Now you can refactor the tests and simplify the User and Note instantiations when the values of username, email, etc do not really matter.

For example you can replace:

.. code-block:: python

    user = User(username='guybrush', email='guybrush@meleeisland.com')
    user.save()

    note = Note(title='Title', owner=user)
    note.save()

    elaine = User(username='elaine', email='elaine@meleeisland.com')
    elaine.save()

    elaine_note = Note(title='Elaine Note Title', owner=elaine)
    elaine_note.save()

by:

.. code-block:: python

    guybrush = UserFactory()
    guybrush_note = NoteFactory(title='Title Guybrush', owner=guybrush)

    elaine = UserFactory()
    elaine_note = NoteFactory(title='Title Elaine', owner=elaine)

You can even create a Note without specifying the owner, since a user will be lazily created.

Don’t forget to commit your changes before going to the next step.
