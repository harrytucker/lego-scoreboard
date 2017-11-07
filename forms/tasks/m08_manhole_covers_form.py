# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import SelectField, BooleanField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class M08ManholeCoversForm(BaseTaskForm):
    title = 'M08 - Manhole Covers'
    info = 'Flip Manhole cover(s) over, obviously past vertical without ' \
           'it/them ever reaching Base.'

    # fields
    covers_flipped = SelectField('Manhold covers flipped:',
                                 choices=[('0', '0'),
                                          ('1', '1'),
                                          ('2', '2')])
    in_separate_targets = BooleanField('Both covers completely in '\
                                       'separate Tripod targets:')


    def points_scored(self) -> int:
        """Calculate the points scored for the task."""
        flipped = int(self.covers_flipped.data)
        # 15 points per cover
        score = flipped * 15

        # if both flipped check they're in separate targets
        if flipped == 2:
            if self.in_separate_targets.data:
                score += 30

        return score
