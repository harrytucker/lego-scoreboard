# -----------------------------------------------------------------------------
# The form used for scoring the active round.
#
# Needs to be updated each year with the new tasks.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import RadioField, BooleanField, SelectField, IntegerField, HiddenField
from wtforms.compat import text_type
from wtforms.validators import InputRequired, Optional


class BonusField(BooleanField):
    def __init__(self, label=None, validators=None, false_values=None, value=None, **kwargs):
        super(BonusField, self).__init__(label, validators, false_values, **kwargs)
        self.value = value


    def _value(self):
        if self.raw_data:
            return text_type(self.raw_data[0])

        if self.value:
            return self.value

        return 'y'


class ScoreRoundForm(FlaskForm):
    m01_title = 'M01 - Space Travel'
    m02_title = 'M02 - Solar Panel Array'
    m03_title = 'M03 - 3D Printing'
    m04_title = 'M04 - Crater Crossing'
    m05_title = 'M05 - Extraction'
    m06_title = 'M06 - Space Station Modules'
    m07_title = 'M07 - Space Walk Emergency'
    m08_title = 'M08 - Aerobic Exercise'
    m09_title = 'M09 - Strength Exercise'
    m10_title = 'M10 - Food Production'
    m11_title = 'M11 - Escape Velocity'
    m12_title = 'M12 - Satellite Orbits'
    m13_title = 'M13 - Observatory'
    m14_title = 'M14 - Meteoroid Deflection'
    m15_title = 'M15 - Landing Touch-Down'
    penalties_title = 'Penalties'

    # fields
    team = SelectField('Team:', validators=[InputRequired(message='Please select a team.')])
    yellow_card = BooleanField('Yellow card')
    confirm = HiddenField(default='0')
    score = IntegerField('Total score', validators=[Optional()])

    m01_complete = RadioField('Send Payload rockets (carts) down the Space Travel Ramp.',
                              choices=[('0', '0 (0 points)'),
                                       ('10', '1 (10 points)'),
                                       ('14', '2 (14 points)'),
                                       ('22', '3 (22 points)'),
                                       ('24', '4 (24 points)'),
                                       ('32', '5 (32 points)'),
                                       ('36', '6 (36 points)'),
                                       ('46', '7 (46 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M01.')])

    m02_complete = RadioField('Solar Panels need to be angled toward or away from you, '
                              'depending on strategy and conditions.',
                              choices=[('0', '0 (0 points)'),
                                       ('18', '1 (18 points)'),
                                       ('22', '2 (22 points)'),
                                       ('40', '3 (40 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M02.')])

    m03_complete = RadioField('The Regolith Core must be placed into the 3D Printer, '
                              'the ejected 2x4 Brick can be delivered for more points.',
                              choices=[('0', '0 (0 points)'),
                                       ('18', '1 (18 points)'),
                                       ('22', '2 (22 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M03')])

    m04_complete = RadioField('The Robot or whatever agent-craft it sends out needs to cross ',
                              'the Craters Model, by driving directly over it.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M04')])

    m05_complete = RadioField('The Robot must get all the Core Samples out of the Core Site.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', '1 (16 points)'),
                                       ('24', '2 (24 points)'),
                                       ('26', '3 (26 points)'),
                                       ('28', '4 (28 points)'),
                                       ('34', '5 (34 points)'),
                                       ('36', '6 (36 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M05')])

    m06_complete = RadioField('The Robot needs to remove and insert Modules among the '
                              'Habitation Hub port holes.',
                              choices=[('0', '0 (0 points)'),
                                       ('14', '1 (14 points)'),
                                       ('16', '2 (16 points)'),
                                       ('30', '3 (30 points)'),
                                       ('32', '4 (32 points)'),
                                       ('46', '5 (46 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M06')])

    m07_complete = RadioField('The Robot needs to get Gerhard’s body into the Airlock Chamber.',
                              choices=[('0', '0 (0 points)'),
                                       ('18', '1 (18 points)'),
                                       ('22', '2 (22 points')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M07')])

    m08_complete = SelectField('The Robot needs to repeatedly move one or both of the '
                               'Exercise Machine’s Handle Assemblies to make the Pointer advance.',
                               choices=[('0', '0 (0 points)'),
                                        ('18', '1 (18 points)'),
                                        ('20', '2 (20 points)'),
                                        ('22', '3 (22 points)')],
                               validators=[Optional()])

    m09_complete = SelectField('The Robot needs to lift the Strength Bar to a scoring heigth.',
                               choices=[('16', 'Yes (16 points)'),
                                        ('0', 'No (0 points)')],
                               validators=[Optional()])

    m10_complete = RadioField('Move the Push Bar to get into the green scoring range.',
                              choices=[('16', 'Yes (16 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M10')])

    m11_complete = SelectField('The Robot needs to impact the Strike Pad hard enough to '
                               'keep the spacecraft from dropping back down.',
                               choices=[('24', 'Yes (24 points)'),
                                       ('0', 'No (0 points)')],
                               validators=[Optional()])

    m12_complete = RadioField('The Robot needs to move one or more Satellites to the Outer Orbit.',
                              choices=[('0', '0 (0 points)'),
                                       ('8', '1 (8 points)'),
                                       ('16', '2 (16 points)'),
                                       ('24', '3 (24 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M12')])

    m13_complete = RadioField('Rotate the Observatory to a precise direction.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', '1 (16 points)'),
                                       ('18', '2 (18 points)'),
                                       ('20', '3 (20 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M13')])

    m14_complete = SelectField('From west of the Free-Line, send one or both Meteoroids '
                                'Independently to the Meteoroid catcher.',
                               choices=[('0', '0 (0 points)'),
                                        ('8', '1 (8 points)'),
                                        ('12', '2 (12 points)'),
                                        ('16', '3 (16 points)'),
                                        ('20', '4 (20 points)'),
                                        ('24', '5 (24 points)'),],
                               validators=[Optional()])

    m15_complete = RadioField('Get the Lander to one of its targets intact, or at least '
                              'get it to Base.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', '1 (16 points)'),
                                       ('20', '2 (20 points)'),
                                       ('22', '3 (22 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M15')])

    penalties_chosen = SelectField('Number of penalties',
                             choices=[('0', '0 (0 points)'),
                                      ('3', '1 (-3 points)'),
                                      ('6', '2 (-6 points)'),
                                      ('9', '3 (-9 points)'),
                                      ('12', '4 (-12 points)'),
                                      ('15', '5 (-15 points)'),
                                      ('18', '6 (-18 points)')],
                             validators=[Optional()])

    def points_scored(self) -> int:
        """Calculate the points scored for this round."""
        score = 0

        score += int(self.m01_complete.data)
        score += int(self.m02_complete.data)
        score += int(self.m03_complete.data)
        score += int(self.m04_complete.data)
        score += int(self.m05_complete.data)
        score += int(self.m06_complete.data)
        score += int(self.m07_complete.data)

        m08_score = int(self.m08_complete.data)
        if m08_score == 30:
            m08_score += int(self.m08_bonus.value if self.m08_bonus.data else 0)
        score += m08_score

        score += int(self.m09_complete.data)
        score += int(self.m10_complete.data)
        score += int(self.m11_complete.data)
        score += int(self.m12_complete.data)

        m13_score = int(self.m13_complete.data)
        if m13_score == 30:
            m13_score += int(self.m13_bonus.value if self.m13_bonus.data else 0)
        score += m13_score

        score += int(self.m14_complete.data)
        score += int(self.m15_complete.data)

        m16_score = int(self.m16_part_1.data)
        m16_score += int(self.m16_part_2.data)
        if int(self.m16_part_2.data) >= 20:
            m16_score += int(self.m16_bonus.value if self.m16_bonus.data else 0)
        score += m16_score

        m17_score = int(self.m17_complete.data)
        if m17_score == 20:
            m17_score += int(self.m17_bonus.value if self.m17_bonus.data else 0)
        score += m17_score

        score += int(self.m18_complete.data)
        score -= int(self.penalties_chosen.data)

        if score < 0:
            score = 0

        return score
