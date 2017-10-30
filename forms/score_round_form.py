# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team', validators=[DataRequired()])
    task = SelectField('Task', validators=[DataRequired()])
