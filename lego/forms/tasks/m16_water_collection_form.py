# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import BooleanField, SelectField
# TODO: Add validators to selectfield?
#from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M16WaterCollectionForm(BaseTaskForm):
    title = 'M16 - Water Collection'
    info = 'Move or catch Big Water and/or Rain water (one Rain maximum; no Dirty Water) so it ' \
           'is touching the mat in the Water Target, without the target ever reaching the ' \
           'white Off-Limits Line shown below. Water may be touching the target, and/or other ' \
           'water, but not be touching nor guided by anything else. Each water model is scored ' \
           'as an individual.'

    # TODO: how to score this?
    # At least one Rain: 10 Points
    # Big Water: 10 Points EACH
    # FOR BONUS: Score at least one Big Water in its target as described above WITH one on top,
    #            which is touching nothing but other water. 30 Points
    #            (Maximum only one Bonus can score)

    # rain = BooleanField('At least one Rain in the target (10 points):')
    # big_water = SelectField('Number of Big Water in target (10 points each)', choices=[('0', '0 (0 points)'), ('1', '1 (10 points)'), ('2', '2 (20 points)')])

    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        return 0
