======
GitLog
======

GitLog is a Django app that create reusable commit-log datas for furthur machining

GitLog parse the `git log` and save them into the Commit table. Which can let you access it and make it full use of in you website.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "gitlog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gitlog',
    ]

2. Include the gitlog URLconf in your project urls.py like this::

    path('gitlog/', include("gitlog.urls", namespace='gitlog')),

3. Run `python manage.py migrate` to create the gitlog models.

4. Start the development server and visit http://127.0.0.1:8000/gitlog/run
   to run the parse precedure.

5. Visit http://127.0.0.1:8000/gitlog/ to see an example Commit Journal.