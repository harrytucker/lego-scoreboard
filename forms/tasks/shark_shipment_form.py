# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField
from wtforms.validators import DataRequired


class SharkShipmentForm(FlaskForm):
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
    touching_floor = BooleanField('Shark touching ONLY Tank floor (NOT wall)',
                                  validators=[DataRequired()])
    nothing_touched = BooleanField('Nothing touched the Shark except the Tank',
                                  validators=[DataRequired()])
