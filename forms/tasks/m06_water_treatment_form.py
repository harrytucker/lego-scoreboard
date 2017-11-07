# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M06WaterTreatmentForm(BaseTaskForm):
    title = 'M06 - Water Treatment'
    info = 'Make the Water Treatment model eject its Big Water, only by moving ' \
           'the Toilet\'s lever'

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
