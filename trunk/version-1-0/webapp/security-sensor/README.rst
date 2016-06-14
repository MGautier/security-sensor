=====
Security sensor
=====

Security sensor is a Django app to process events log from different security source.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "secapp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'secapp',
    ]

2. Include the secapp URLconf in your project urls.py like this::

    url(r'^secapp/', include('secapp.urls')),

3. Run `python manage.py migrate` to create the secapp models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user isolated like user-secapp (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/secapp/ to see events log in a chart.
