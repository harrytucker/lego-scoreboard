# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import Optional


class StageForm(FlaskForm):
    stage = SelectField('Move to stage:',
                        choices=[('0', 'First Round'),
                                 ('1', 'Quarter Final'),
                                 ('2', 'Semi Final'),
                                 ('3', 'Final')],
                        validators=[Optional()])
