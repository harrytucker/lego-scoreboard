# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class EditTeamForm(FlaskForm):
    id = HiddenField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired()])
