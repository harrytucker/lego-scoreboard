# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class BaseTaskForm(FlaskForm):
    title = 'Not set'
    info = 'Not set'

    # common fields between forms
    team = HiddenField('Team id', validators=[DataRequired()])
    task = HiddenField('Task id', validators=[DataRequired()])

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        raise NotImplementedError('Method not implemented by parent class.')
