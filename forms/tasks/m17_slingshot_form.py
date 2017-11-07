# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M17SlingshotForm(BaseTaskForm):
    title = 'Not set'
    info = 'Not set'

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        super()
