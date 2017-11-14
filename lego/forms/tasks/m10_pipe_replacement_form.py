# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M10PipeReplacementForm(BaseTaskForm):
    title = 'M10 - Pipe Replacement'
    info = 'Move a New Pipe so it is where the broken one started, in full/flat contact with ' \
           'the mat. You may install the Optional Loop first, in Base, if you wish.'

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
