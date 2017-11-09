# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired

from lego.forms.tasks import TASK_FORMS


def _task_choices() -> list:
    choices = [('', '--Select task--')]
    choices += [(i, t.title) for i, t in enumerate(TASK_FORMS)]

    return choices


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team', validators=[InputRequired()])
    task = SelectField('Task',
                       choices=_task_choices())
