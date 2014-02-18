Let's implement a note edition view
===================================

Let's implement a note edition view. Again, you should use a class based view.
User should only be able to edit the note title and content. Let's say the creation date and the owner cannot be edited.

You will need to use an html form this time:

.. code-block:: html

    <form method="post" id="edit-note-form">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update">
    </form>

Note the {% csrf_token %}. Look in Django documentation what this is about.

Here is a test example for this view. Note that you retrieve the form by its id. You could access response.forms[0] but then if you add another form in your page your test will break.
So it is a good practice to always retrieve a form via its unique id.

.. code-block:: python

    def test_edit_note_not_authenticated(self):
        note = NoteFactory()

        url = reverse('edit_note', args=[note.id])
        response = self.app.get(url, user=note.owner)

        form = response.forms['edit-note-form']
        new_title = 'Updated Title'
        form['title'] = new_title
        new_content = 'Updated content.'
        form['content'] = new_content

        response = form.submit().follow()
        self.assertContains(response, new_title)
        self.assertContains(response, new_content)

Don’t forget to commit your changes before going to the next step.
