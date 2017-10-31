# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired


class ServiceDogActionForm(FlaskForm):
    title = 'M02 Service Dog Action'
    info = 'Robot must cross fence from West, between barriers'

    # fields
    fence_down = BooleanField('Warning fence is down',
                              validators=[DataRequired()])
    crossed_fence = BooleanField('Robot completely crossed fence',
                                 validators=[DataRequired()])
