# Manual
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

As an example, the 2018 guide can be found [here](https://firstinspiresst01.blob.core.windows.net/fll/hydro-dynamics-challenge-guide-a4.pdf)

## Common Issues
- A simple way to check the setup has been performed correctly is to run `flask --help`. If everything is fine, you will see multiple commands listed in addition to the standard `flask run` and `flask shell`. If you do not see these, run `flask shell` and the error should be returned.
- If you see an error similar to `AttributeError: 'module' object has no attribute 'config'` on a page when the application is running, simply restart the application. This can happen when an exception occurs such as an ImportError of SyntaxError and the application gets stuck.
- Error and debug logs can be found in the `lego/logs/` directory. If the error is not output to the GUI or commandline, it will be output in at least one of the log files.

## Tips
- To view the database in it's raw form, `sqlite3` can be used. To do so, simply run `sqlite3 /app/lego/tmp/lego.db`. The sqlite3 specific commands that can be run can be found using `.help`. SQL queries work in much the same way as other dialects which can be found in various guides available online. Examples of queries you may want to run are:
    - Updating the user passwords: These are stored in plaintext, so can be changed with a simple `UPDATE` statement.
    - Debugging an operation: simply run `.dump` to get the full database output. More granular queries can be created using a `SELECT` statement.
- The current stage is persisted to a file and cannot be moved backwards through the GUI. However, it can be manually edited if necessary and should be a value of 0-3 representing the first round through to the final. Note that if you do manually go back a stage then you will need to set the `active` column manually for the relevant teams, e.g. `UPDATE team SET active=1 WHERE is_practice=0;`.
