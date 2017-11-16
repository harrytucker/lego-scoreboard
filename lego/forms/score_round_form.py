# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired

from lego.forms.tasks import TASK_FORMS
from lego.models import Team


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team:', validators=[InputRequired()])
    task = SelectField('Task:', validators=[InputRequired()])
