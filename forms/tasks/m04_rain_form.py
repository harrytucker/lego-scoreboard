# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M04RainForm(BaseTaskForm):
    title = 'M04 - Rain'
    info = 'Make at least one Rain come out of the Rain Cloud.'

    # fields
    task_complete = RadioField('Task complete:',
        choices=[('y', 'Yes (20 points)'),
                 ('n', 'No (0 points)')],
        validators=[InputRequired('Please make a choice for Task complete')])


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        if self.task_complete.data == 'y':
            return 20

        return 0
