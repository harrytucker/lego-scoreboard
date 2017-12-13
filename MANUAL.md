# Maintenance Guide
This application has been built with the idea that it will be passed on to future maintainers. For example, Flask was chosen because it is written in a commonly taught language and has a number of guides and help resources available.

## Resources
The following resources were used to create the original application which may be of use for future updates or answer questions about how certain parts work:

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

Flask also provides a number of quickstart guides for both the main Flask module and it's supported extensions. Many of the extensions wrap pre-existing modules. The following pages may also be of use when updating the code:

- [Flask](http://flask.pocoo.org/) ([Quickstart](http://flask.pocoo.org/docs/0.12/quickstart/))
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) ([Quickstart](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/))
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) ([Quickstart](http://flask-wtf.readthedocs.io/en/stable/quickstart.html))
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [WTForms](https://wtforms.readthedocs.io/en/latest/)
- [Jinja2](http://jinja.pocoo.org/docs/2.9/)
- [Click](http://click.pocoo.org/5/)

## Updating Tasks
Each year has different tasks thus the application need to be updated to handle them. the following files will need to be updated:
- `templates/base.html`: Change the year of the competition.
- `forms/score_round_form.py`: Replace the fields in the form to the new tasks and adjust the `points_scored` method accordingly.
- `templates/judges/score_round.html`: Update the template with the fields from the updated form.

## Notes
- [2018 Challenge guide](https://firstinspiresst01.blob.core.windows.net/fll/hydro-dynamics-challenge-guide-a4.pdf)

## Errors
- A simple way to check the setup has been performed correctly is to run `flask --help`. If everything is fine, you will see multiple commands listed in addition to the standard `flask run` and `flask shell`. If you do not see these, run `flask shell` and the error should be returned.
- If you see an error similar to `AttributeError: 'module' object has no attribute 'config'` on a page when the application is running, simply restart the application. This happens when another error occurred and the initial application configuration gets stuck.
