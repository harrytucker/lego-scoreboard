# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M10PipeReplacementForm(BaseTaskForm):
    title = 'M10 - Pipe Replacement'
    info = '(Install the Optional Loop first, in Base, if you wish.) ' \
           'Move a New Pipe so it is here the broken one started, in ' \
           'full/flat contact with the mat.'

    # fields
    pipe_replaced = BooleanField('Pipe replaced')


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        if self.pipe_replaced.data:
            return 20
