# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class BaseTaskForm(FlaskForm):
    # common fields between forms
    team = HiddenField('Team id', validators=[DataRequired()])
    task = HiddenField('Task id', validators=[DataRequired()])
