
Welcome to django-gitlog's documentation!
=========================================

 This is an app that parse your git log and save it in database.
 You can turn it into a develope journal.

Requirement
-----------
Django 2.2.9 (former vertion is untested)
Git (make sure it's an git repo already.)


Quickstart
----------

1. Add "gitlog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gitlog',
    ]


2. Include the gitlog URLconf in your project urls.py like this::

    path('gitlog/', include("gitlog.urls", namespace='gitlog')),

3. Run `python manage.py migrate` to create the gitlog models.

4. Start the development server and visit http://127.0.0.1:8000/gitlog/run to run the parse precedure.

5. Visit http://127.0.0.1:8000/gitlog/ to see an example Commit Journal.

Trouble shooting
----------------
If you got error of::

   returning non 0 code

try to run git log in your own shell and see if anything get wrong.


.. toctree::
   :maxdepth: 2

   LICENSE



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`