# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

from lego.forms.tasks import TASK_FORMS


def _task_choices() -> list:
    choices = [('-2', '--Select task--')]
    choices += [(i + 1, t.title) for i, t in enumerate(TASK_FORMS)]

    return choices


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team', validators=[DataRequired()])
    task = SelectField('Task',
                       coerce=int,
                       choices=_task_choices(),
                       validators=[DataRequired()])
