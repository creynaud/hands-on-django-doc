Let's implement a 1st view: the home page
=========================================

To implement the home view, we will need to write a bit of html and a bit of python code.

So far we just want the home view to display a custom welcome message.
Let's uncomment the following line in notes/urls.py:

.. code-block:: python

    # url(r'^$', 'notes.views.home', name='home'),

Then let's create a notes/views.py file, and add a view function for our home page:

.. code-block:: python

    from django.http.response import HttpResponse


    def home(request):
        return HttpResponse('Welcome!')

Have a look at http://127.0.0.1:8000/, you should see the Welcome! message.

Ok, cool, but this is not an html page. Let's create an html file for this home page.

Create a file named index.html. It should reside in notes/templates/notes/ under your project root directory, so create the intermediate folders too.

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h1>Welcome!</h1>
        <p>This is the Notes App. Django powered!</p>
    </body>
    </html>

Let's make our home view render this template instead of our 'Welcome!' string, so let's modify our home view function.

.. code-block:: python

    from django.http.response import HttpResponse
    from django.template import loader
    from django.template.context import RequestContext


    def home(request):
        template = loader.get_template('notes/index.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))

Have a look at http://127.0.0.1:8000/, you should see an error message saying the html template file cannot be found.

We need to tell Django were to look for our html template, so add the following lines at the end of the settings.py file:

.. code-block:: python

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'notes/templates'),
    )

Refresh http://127.0.0.1:8000/. Your home page should render correctly now.

So far we only rendered a static html page. We don't need Django for that ;). So let's modify our view again to see how showing dynamic content.
Let's add a date in the context used to render the template:

.. code-block:: python

    from django.http.response import HttpResponse
    from django.template import loader
    from django.template.context import RequestContext
    from django.utils import timezone


    def home(request):
        template = loader.get_template('notes/index.html')
        context = RequestContext(request, {'date': timezone.now()})
        return HttpResponse(template.render(context))

And let's modify the template too:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Notes App</title>
    </head>
    <body>
    <h1>Welcome{% if user.is_authenticated %} {{ user.email }}{% endif %}!</h1>

    <p>This is the Notes App. Django powered!</p>

    <p>{{ date }}</p>
    </body>
    </html>

Refresh http://127.0.0.1:8000/. Your home page shows some dynamic content now.
