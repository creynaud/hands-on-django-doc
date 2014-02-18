My Notes class based view
=========================

So far we've been implementing views by writing functions. But with Django you can also define a view with a class.
Django provides a hierarchy of classes, the class based views (sometimes called CBVs - https://docs.djangoproject.com/en/dev/topics/class-based-views/), that implements common views like detail view, creation view, list view out of the box.
By using class based views instead of functions, you are likely to write less code.

So let's modify the notes view and implement it with a class based view. Here is the new code for the view.

.. code-block:: python

    from django.views.generic.list import ListView

    from .models import Note


    class Notes(ListView):
        model = Note
        template_name = 'notesapp/notes.html'
        context_object_name = 'notes'

        def get_queryset(self):
            return Note.objects.all()
    notes = Notes.as_view()

Run the tests and verify the notes view tests still pass.

Now let's say we want notes to be private. So only the owner of the note should be able to see his notes.
Let's refactor this view, rename it my_notes, and list only the notes of the logged in user. You will have to modify the queryset and add a decorator to the view (login_required).

.. code-block:: python
    :emphasize-lines: 1,13

    +from django.contrib.auth.decorators import login_required
     from django.views.generic.list import ListView

     from .models import Note


     class MyNotes(ListView):
         model = Note
         template_name = 'notesapp/my_notes.html'
         context_object_name = 'notes'

         def get_queryset(self):
     +       return Note.objects.filter(owner=self.request.user)
    +my_notes = login_required(MyNotes.as_view())


You can login/logout via the admin (http://127.0.0.1:8000/admin/) to see what happens when you access the view when you are logged in or not.
What happens when you access http://127.0.0.1:8000/notes/ and you are not logged in (hint: this will be the subject of the next step of this workshop)?

Don't forget to modify the tests accordingly.

Also commit your changes before going to the next step.
