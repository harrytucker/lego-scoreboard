# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import SelectField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M09TripodForm(BaseTaskForm):
    title = 'M09 - Tripod'
    info = 'Move the inspection camera Tripod so it is in either Tripod ' \
           'target, with all of its feet touching the mat.'

    # fields
    in_target = SelectField('In target',
                            coerce=int,
                            choices=[('0', 'Not in Tripod'),
                                     ('15', 'Partially in Tripod'),
                                     ('20', 'Completely in Tripod')])


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        return self.in_target.data
