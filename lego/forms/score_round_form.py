# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired

from lego.forms.tasks import TASK_FORMS
from lego.models import Team


def _team_choices() -> list:
    choices = [('', '--Select team--'), ('-1', 'PRACTICE')]
    choices += [(str(t.id), t.name) for t in Team.query.order_by('name')]

    return choices

def _task_choices() -> list:
    choices = [('', '--Select task--')]
    choices += [(str(i), t.title) for i, t in enumerate(TASK_FORMS)]

    return choices


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team:',
                       choices=_team_choices())
    task = SelectField('Task:',
                       choices=_task_choices())
