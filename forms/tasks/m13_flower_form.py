# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M13FlowerForm(BaseTaskForm):
    title = 'M13 - Flower'
    info = 'Make the Flower rise some obvious height and stay there, due only to a Big Water in ' \
           'the brown pot. For bonus points, Score Flower Points as described above with at ' \
           'least one Rain in the purple part, touching nothing but the Flower model.'

    # fields
    task_complete = RadioField('Task complete:',
        choices=[('y', 'Yes (30 points)'),
                 ('n', 'No (0 points)')],
        validators=[InputRequired('Please make a choice for Task complete')])
    bonus = BooleanField('At least one Rain in the purple part (30 bonus points):')


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        score = 0

        if self.task_complete.data == 'y':
            score = 30

            if self.bonus.data:
                score += 30

        return score
