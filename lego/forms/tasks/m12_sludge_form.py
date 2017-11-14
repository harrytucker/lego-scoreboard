# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M12SludgeForm(BaseTaskForm):
    title = 'M12 - Sludge'
    info = 'Move the Sludge so it is touching the visible wood of any of the six drawn garden ' \
           'boxes.'

    # fields
    task_complete = RadioField('Task complete:',
        choices=[('y', 'Yes (30 points)'),
                 ('n', 'No (0 points)')],
        validators=[InputRequired('Please make a choice for Task complete')])


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        if self.task_complete.data == 'y':
            return 30

        return 0
