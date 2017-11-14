# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M02FlowForm(BaseTaskForm):
    title = 'M02 - Flow'
    info = 'Move a Big Water (one time maximum) to the other team\'s field ' \
           'only by turning the Pump System\'s valve(s).'

    # fields
    task_complete = RadioField('Task complete:',
        choices=[('y', 'Yes (25 points)'),
                 ('n', 'No (0 points)')],
        validators=[InputRequired('Please make a choice for Task complete')])


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        if self.task_complete.data == 'y':
            return 25

        return 0
