===============
Django Spikeval
===============

Datafile is a simple Django app that adds generic file assets that
can be referenced and used by other applications by generic foreign
keys. The general `datafile` does not make any assumptions about the
nature of the file and stores it in a filesystem backend.

Detailed documentation is in the "docs" directory. [todo: perhaps later]

Quick start
-----------

1. Add "datafile" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'spikeval',
      )

2. Include the polls URLconf in your project urls.py like this::

      url(r'^spikeval/', include('spikeval.urls')),

3. Run `python manage.py syncdb` to create the spikeval models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create and/or manage any spikeval entities (you'll need the Admin
   app enabled).

5. Visit http://127.0.0.1:8000/spikeval/ to browse `spikeval` assets.
