Let's implement views to add and delete notes
=============================================

Here is how you can implement the view to add a note. It's a little bit more complex than the edit view because you need to set the note owner.
Let's pass the request's user to a NoteCreationForm:

.. code-block:: python

    from django.shortcuts import redirect

    from .forms import NoteCreationForm

    ............

    class AddNote(UserNotesInContextMixin, CreateView):
        model = Note
        fields = ['title', 'content']
        form_class = NoteCreationForm
        template_name = 'notesapp/add_note.html'

        def form_valid(self, form):
            self.object = form.save(owner=self.request.user)
            return redirect(self.object.get_absolute_url())
    add_note = login_required(AddNote.as_view())

Create a new notesapp/forms.py file containing the new form class:

.. code-block:: python

    from django import forms

    from .models import Note


    class NoteCreationForm(forms.ModelForm):
        class Meta:
            model = Note
            fields = ['title', 'content']

        def save(self, owner=None, commit=True):
            note = super(NoteCreationForm, self).save(commit=False)
            note.owner = owner
            note.save()
            return note

Don't forget to write some tests for the new note creation view. You can take the note edition view tests as an example.

Also add a view to delete notes, with tests too.

Don’t forget to commit your changes before going to the next step.

