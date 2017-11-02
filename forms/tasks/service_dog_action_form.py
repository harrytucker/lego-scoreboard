# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class ServiceDogActionForm(BaseTaskForm):
    title = 'M02 Service Dog Action'
    info = 'Robot must cross fence from West, between barriers'

    # fields
    fence_down = BooleanField('Warning fence is down',
                              validators=[DataRequired()])
    crossed_fence = BooleanField('Robot completely crossed fence',
                                 validators=[DataRequired()])

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        if self.crossed_fence.data:
            if self.fence_down.data:
                return 15

        return 0
