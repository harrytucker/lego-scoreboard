# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField, SelectField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class SharkShipmentForm(BaseTaskForm):
    title = 'M01 Shark Shipment'
    info = 'Nothing can touch the Shark except the tank'

    # fields
    in_target = SelectField('Shark and Tank are completely in Target',
                            coerce=int,
                            choices=[
                                ('0', 'None (0 points)'),
                                ('7', 'Target One (7 points)'),
                                ('10', 'Target Two (10 points)'),
                            ],
                            validators=[DataRequired()])
    touching_floor = BooleanField('Shark touching ONLY Tank floor (NOT wall)')
    nothing_touched = BooleanField('Nothing touched the Shark except the Tank')

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        score = 0

        if self.nothing_touched.data:
            score = int(self.in_target.data)

            if self.touching_floor.data:
                score += 20

        return score
