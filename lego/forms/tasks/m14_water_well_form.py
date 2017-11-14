# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import SelectField
# TODO: Add validators to selectfield?
#from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M14WaterWellForm(BaseTaskForm):
    title = 'M14 - Water Well'
    info = 'Move the Water Well so it has contact with the mat and that contact is in the Water ' \
           'Well target.'

    # fields
    in_target = SelectField('In target:',
                            choices=[('0', 'Not in target (0 points)'),
                                     ('15', 'Partially in target (15 points)'),
                                     ('25', 'Completely in target (25 points)')])

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        return int(self.in_target.data)
