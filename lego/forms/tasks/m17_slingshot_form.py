# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField, RadioField
from wtforms.validators import InputRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M17SlingshotForm(BaseTaskForm):
    title = 'M17 - Slingshot'
    info = 'Move the SlingShot so it is completely in its target. for bonus points, Score ' \
           'SlingShot points as described above WITH the Dirty Water and a Rain completely in ' \
           'the SlingShot target.'

    # fields
    task_complete = RadioField('Task complete:',
        choices=[('y', 'Yes (20 points)'),
                 ('n', 'No (0 points)')],
        validators=[InputRequired('Please make a choice for Task complete')])
    bonus = BooleanField('Dirty Water and a Rain completely in the target (15 bonus points):')


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        score = 0

        if self.task_complete.data == 'y':
            score = 20

            if self.bonus.data:
                score += 15

        return score
