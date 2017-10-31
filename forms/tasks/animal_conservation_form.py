# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from wtforms import SelectField
from wtforms.validators import DataRequired

from lego.forms.tasks.base_task_form import BaseTaskForm


class AnimalConservationForm(BaseTaskForm):
    title = 'M03 Animal Conservation'
    info = 'Pairs made by rotation of model'

    # fields
    animal_pairs = SelectField('Pairs of identical animals completely on same side (both fields)',
                             choices=[
                                ('0', '0'),
                                ('20', '1 (20 points)'),
                                ('40', '2 (40 points)'),
                                ('60', '3 (60 points)'),
                                ('80', '4 (80 points)'),
                                ('100', '5 (100 points)'),
                                ('120', '6 (120 points)')
                             ],
                             validators=[DataRequired()])
