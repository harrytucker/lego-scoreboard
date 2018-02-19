# Manual
This application has been built with the idea that it will be passed on to future maintainers.

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
- If you see an error similar to `AttributeError: 'module' object has no attribute 'config'` on a page when the application is running, simply restart the application. This can happen when an exception occurs such as an ImportError or SyntaxError and the application gets stuck.
- Logs for the application can be found in the `lego/logs/app.log` directory. If the error is not output to the GUI or commandline, it will be output to the log file.

## Tips
- To view and/or modify the database in it's raw form, `sqlite3` can be used (requires SQLite 3 to be installed first). To do so, simply run `sqlite3 /app/lego/tmp/app.db`. The sqlite3 specific commands that can be run can be found using `.help`. SQL queries work in much the same way as other dialects which can be found in various guides available online. Examples of queries you may want to run are:
    - Updating the user passwords: These are stored in plaintext, so can be changed with a simple `UPDATE` statement.
    - Debugging an operation: Simply run `.dump` to get the full database output, or `.dump <tablename>` to view the schema and current data for a specific table. More granular queries can be created using a `SELECT` statement.
    - Viewing a table's schema: User `.schema [tablename]` to view the schemas for the entire database or a single table by not setting or setting `tablename` respectively.
- The current stage is persisted to a file and cannot be moved backwards through the GUI. However, it can be set using the `flask stage` command in the CLI or manually edited and should be a value of 0-4 representing the first round through to the final. Note that if you do manually go back a stage then you will need to set the relevant teams to active. For more informaion, see the Stages section.

## Configuration
A sample configuration file can be found at `config.sample.py` which should be copied to `config.py` for local modifications. The following configuration options are currently in use:

- `WTF_CSRF_ENABLED`: Eanbles CSRF protection. the was added due to the tiny amount of extra code required and the small security improvement it adds. Should not need to be modified.
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Enables transaction logging. Turned off as it isn't necessary for this application. Should not need to be modified.
- `SQLALCHEMY_DATABASE_URI`: The path to the SQLite3 database file. This is `lego/tmp/app.db`. Should not need to be modified.
- `SECRET_KEY`: The secret key used to sign session cookies. Should be set during the application setup (see README.md)
- `LEGO_APP_TYPE`: The application type. Supports `'bristol'`, for use in the Bristol final, and `'uk'`, for use in the UK final. the main differences are the customisations to the scoreboard due to the different format of the finals and number of teams.

## Database
The database layout is below. the metadata key is:
- `PK`: Primary key.
- `U`: Unique value. This may be enforced by the aplication or the database.

### User

| Metadata | Column   | Type                 | Description |
| -------- | -------- | -------------------- | ----------- |
| PK       | id       | INTEGER NOT NULL     | The user id. For internal use. |
| U        | username | VARCHAR(80) NOT NULL | The user's username. For logging in. |
|          | password | VARCHAR(80) NOT NULL | The user's password. For logging in. |
|          | is_judge | BOOLEAN NOT NULL     | If the user is a judge. Grants access to judge pages. |
|          | is_admin | BOOLEAN NOT NULL     | If the user is an admin. Grants access to judge and admin pages. |

### Team

| Metadata | Column      | Type             | Description |
| -------- | ----------- | ---------------- | ----------- |
| PK       | id          | INTEGER NOT NULL | The team id. For internal use. |
| U        | number      | INTEGER NOT NULL | The team's number. Used to identify the team. |
| U        | name        | VARCHAR(80)      | The team's name. Used to identify the team. |
|          | active      | BOOLEAN NOT NULL | Whether the team is currently active and should appear on the scoreboard. |
|          | is_practice | BOOLEAN NOT NULL | Whether the team is a practice team for judge training. |
|          | attempt_1   | INTEGER          | The team's score for Round 1 - Attempt 1. |
|          | attempt_2   | INTEGER          | The team's score for Round 1 - Attempt 2. |
|          | attempt_3   | INTEGER          | The team's score for Round 1 - Attempt 3. |
|          | round_2     | INTEGER          | The team's score for Round 2. |
|          | quarter     | INTEGER          | The team's score for the Quarter Final. |
|          | semi        | INTEGER          | The team's score for the Semi Final. |
|          | final_1     | INTEGER          | The team's score for the Final - Part 1. |
|          | final_2     | INTEGER          | The team's score for the Final - Part 2. |


## Command Line Interface
The base flask CLI has been extended with a number of commands specific to this application. For a full list see `flask --help`. The following commands have been added. Their documentation is available using `flask <command> --help`.

- `init`
- `secret`
- `add-teams`
- `list-teams`
- `reset-teams`
- `stage`
- `simulate` - Covered in more detail below.

## Stages
A stage identfies the current place in the competition. It can take one of 5 values, represented as the following numbers internally:

0. Round 1
1. Round 2 (UK Final only)
2. Quarter Final
3. Semi Final
4. Final

The current stage dictates how much information to display on the scoreboard. For example, Round 1 will only display scores for Round 1. Later stages will display scores from the current stage and any previous stages. Only teams that are designated as active will appear on the scoreboard and be available for scoring via the judges score round page. When the stage progresses, a number of teams will be marked as inactive denoting that they will not progress to the next stage.

There is a built in mechanism for moving the stage forwards in the admin pages. If you need to move the stage back you will need to do so manually. This requires two steps:

- Use the `flask stage` CLI command to manually set the stage. Alternatively, edit the file containing the current stage. This can be found in `lego/tmp/.stage`.
- Edit the active teams using the `Manage Active Teams` admin page. This step can also be managed through database access and involves setting the `active` column to 1 or 0 to indicated whether a team is active or not.


## Pages
- Home: Shows a list of teams and their numbers.
- Scoreboard: Shows the current active teams, their numbers and their scores.
- Login: A login page for admins and judges. Login is required to access the admin and judge only pages.

### Judge Pages
- Home: Shows a list of all non-practice teams and their scores. This page also contains a link to export all the score data as a CSV file which can be opened using Microsoft Excel or other spreadsheet software.
- Score Round: A form for calculating and submitting a team's score for a give attempt.

### Admin Pages
- View Teams: Displays a list of teams with links to the following pages:
    - Edit Team Number: Alter the team's number. Note that numbers must be unique so if there is a mix-up, you will need to move one team to a temporary number, move the other team to the correct number then correct the first team's number.
    - Edit Team Score: For editing the score of a specific attempt made by a team. This is for the correction of a score if it was submitted incorrectly by a judge.
    - Reset Team Score: this removes the score for a specific attempt made by a team. Allows the attempt to be re-marked by a judge.
- Add Team: For adding a new team. For bulk team creation, use the CLi command `add-teams`.
- Manage Stage: For managing the current stage. It is only possible to move forward a stage through this page. For moving back a stage, see the instructions in the Stages section above.
- Manage Active Teams: For managing the current active teams. This is for use when the automated algorithm for sorting teams and marking them as (in)active after the stage has been moved forward is inadequate or faulty, allowing for manual correction.

## Simulation
Using `flask simulate`, you can simulate a day's event in a few short minutes. this is intended for checking the scoreboard works correctly. Whle it is functional, note that is it essentially a mash-up of existing functionality and is not particularly inuitive to use.

After starting the command, a script will complete each stage in it's coponent parts, pausing for confirmation to move to the next, i.e. Round 1-1, Round 1-2, Round 1-3, Round 2, Quarter Final, etc. After the script has paused, you can check the scoreboard to check it is working as intended before continuing.

Be aware that simulations will empty the teams database before and after the the script is run to ensure a clean completion. Please ensure that you do not overwrite real data when running the simulation.
