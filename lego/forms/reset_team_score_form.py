# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField
from wtforms.validators import DataRequired


class ResetTeamScoreForm(FlaskForm):
    id = HiddenField('Id', validators=[DataRequired()])
    stage = SelectField('Stage',
                        choices=[('1', 'Round 1'),
                                 ('2', 'Round 2'),
                                 ('3', 'Round 3'),
                                 ('4', 'Quarter-final'),
                                 ('5', 'Semi-final'),
                                 ('6', 'Final - first game'),
                                 ('7', 'Final - second game')],
                        default='1',
                        validators=[DataRequired()])
