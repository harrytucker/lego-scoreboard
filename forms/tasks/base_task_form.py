# -----------------------------------------------------------------------------
# Base task form containing common fields and methods that child form classes
# should implement.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import HiddenField, BooleanField
from wtforms.validators import DataRequired


class BaseTaskForm(FlaskForm):
    title = 'Not set'
    info = 'Not set'

    # common fields between forms
    team = HiddenField('Team id', validators=[DataRequired()])
    task = HiddenField('Task id', validators=[DataRequired()])
    yellow_card = BooleanField('Yellow card')

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        raise NotImplementedError('Method not implemented by parent class.')
