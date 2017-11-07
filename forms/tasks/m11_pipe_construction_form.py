# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import SelectField
# TODO: Add validators to selectfield?
#from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M11PipeConstructionForm(BaseTaskForm):
    title = 'M11 - Pipe Construction'
    info = 'Move a New Pipe so it is in its target and in full/flat contact with the mat.'

    # fields
    in_target = SelectField('In target:',
                            choices=[('0', 'Not in target (0 points)'),
                                     ('15', 'Partially in target (15 points)'),
                                     ('20', 'Completely in target (20 points)')])

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        return int(self.in_target.data)
