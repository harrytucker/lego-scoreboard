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
                              choices=[('0', '(0 points)'),
                                       ('10', 'Crew Payload (10 points)'),
                                       ('14', 'Supply Payload (14 points)'),
                                       ('22', 'Vehicle Payload (22 points)'),
                                       ('24', 'Crew Payload + Supply Payload (24 points)'),
                                       ('32', 'Crew Payload + Vehicle Payload (32 points)'),
                                       ('36', 'Supply Payload + Vehicle Payload (36 points)'),
                                       ('46', 'All Payloads (46 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M01.')])

    m02_complete = RadioField('Solar Panels need to be angled toward or away from you, '
                              'depending on strategy and conditions.',
                              choices=[('0', '(0 points)'),
                                       ('18', '(18 points)'),
                                       ('22', '(22 points)'),
                                       ('40', '(40 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M02.')])

    m03_complete = RadioField('The Regolith Core must be placed into the 3D Printer, '
                              'the ejected 2x4 Brick can be delivered for more points.',
                              choices=[('0', 'Core not placed in printer (0 points)'),
                                       ('18', 'Ejected and partially in planet area (18 points)'),
                                       ('22', 'Ejected and completely in planet area (22 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M03')])

    m04_complete = RadioField('The Robot or whatever agent-craft it sends out needs to cross '
                              'the Craters Model, by driving directly over it.',
                              choices=[('20', 'Yes, travelled East to West, completely past the flattened gate (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M04')])

    m05_complete = RadioField('The Robot must get all the Core Samples out of the Core Site.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', 'All samples moved no longer touching axle (16 points)'),
                                       ('24', 'All samples moved and water core supported only by food growth chamber (24 points)'),
                                       ('26', 'All samples moved and Gas Core completely in base (26 points)'),
                                       ('28', 'All four moved and Gas Core is touching the mat and in landers target circle (28 points)'),
                                       ('34', 'All four moved and Gas core in Base and Water Core is supported only by Food Growth Chamber (34 points)'),
                                       ('36', 'All four moved and Gas core in Target Circle and Water Core is supported only by Food Growth Chamber (36 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M05')])

    m06_complete = RadioField('The Robot needs to remove and insert Modules among the '
                              'Habitation Hub port holes.',
                              choices=[('0', '0 (0 points)'),
                                       ('14', 'Dock Module in the Habitation Hub port, east side (14 points)'),
                                       ('16', 'Tube Module in the Habitation Hub port, west side: (16 points)'),
                                       ('30', 'Dock Module in east side, plus Cone Module in base or Tube Module in west side (30 points)'),
                                       ('32', 'Cone Module completely in Base and Tube Module in Habitation Hub west side (32 points)'),
                                       ('46', 'Cone Module completely in Base and Dock and Tube modules in east side and west sides consequetively (46 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M06')])

    m07_complete = RadioField('The Robot needs to get Gerhard’s body into the Airlock Chamber.',
                              choices=[('0', '0 (0 points)'),
                                       ('18', 'Gerhard’s body partially in airlock chamber (18 points)'),
                                       ('22', 'Gerhard’s body completely in airlock chamber (22 points')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M07')])

    m08_complete = SelectField('The Robot needs to repeatedly move one or both of the '
                               'Exercise Machine’s Handle Assemblies to make the Pointer advance.',
                               choices=[('0', '0 (0 points)'),
                                        ('18', 'Pointer completely in gray, or partly covering either of gray’s end-borders (18 points)'),
                                        ('20', 'Pointer completely in white (20 points)'),
                                        ('22', 'Pointer completely in orange, or partly covering either of orange’s end-borders (22 points)')],
                               validators=[InputRequired('Please make a choice for M08')])

    m09_complete = SelectField('The Robot needs to lift the Strength Bar to a scoring height.',
                               choices=[('16', 'Yes (16 points)'),
                                        ('0', 'No (0 points)')],
                               validators=[InputRequired('Please make a choice for M09')])

    m10_complete = RadioField('Move the Push Bar to get into the green scoring range.',
                              choices=[('16', 'Yes (16 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M10')])

    m11_complete = SelectField('The Robot needs to impact the Strike Pad hard enough to '
                               'keep the spacecraft from dropping back down.',
                               choices=[('24', 'Yes (24 points)'),
                                       ('0', 'No (0 points)')],
                               validators=[InputRequired('Please make a choice for M11')])

    m12_complete = RadioField('The Robot needs to move one or more Satellites to the Outer Orbit.',
                              choices=[('0', '0 (0 points)'),
                                       ('8', '1 moved between the two lines of the Outer Orbit(8 points)'),
                                       ('16', '2 moved between the two lines of the Outer Orbit(16 points)'),
                                       ('24', '3 moved between the two lines of the Outer Orbit(24 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M12')])

    m13_complete = RadioField('Rotate the Observatory to a precise direction.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', 'Tip completely in gray, or partly covering either of gray’s end-borders (16 points)'),
                                       ('18', 'Tip completely in white (18 points)'),
                                       ('20', 'Tip completely in orange, or partly covering either of orange’s end-borders (20 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M13')])

    m14_complete = SelectField('From west of the Free-Line, send one or both Meteoroids '
                                'Independently to the Meteoroid catcher.',
                               choices=[('0', '0 (0 points)'),
                                        ('8', 'Meteoroid in Either Side Section (8 points)'),
                                        ('12', 'Meteoroid in the Center Section (12 points)'),
                                        ('16', 'Both in Sides (16 points)'),
                                        ('20', 'Side and Center (20 points)'),
                                        ('24', 'Both in Center (24 points)'),],
                               validators=[InputRequired('Please make a choice for M14')])

    m15_complete = RadioField('Get the Lander to one of its targets intact, or at least '
                              'get it to Base.',
                              choices=[('0', '0 (0 points)'),
                                       ('16', 'Both parts of the Lander completely into Base (16 points)'),
                                       ('20', 'Lander  intact, touching the Mat, and completely in the Northeast Planet Area (20 points)'),
                                       ('22', 'Lander intact, touching the Mat, and completely in its Target Circle (22 points)')],
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

    def points_scored(self) -> (int, str):
        """Calculate the points scored for this round."""

        score_breakdown = {
            'm01_score': int(self.m01_complete.data),
            'm02_score': int(self.m02_complete.data),
            'm03_score': int(self.m03_complete.data),
            'm04_score': int(self.m04_complete.data),
            'm05_score': int(self.m05_complete.data),
            'm06_score': int(self.m06_complete.data),
            'm07_score': int(self.m07_complete.data),
            'm08_score': int(self.m08_complete.data),
            'm09_score': int(self.m09_complete.data),
            'm10_score': int(self.m10_complete.data),
            'm11_score': int(self.m11_complete.data),
            'm12_score': int(self.m12_complete.data),
            'm13_score': int(self.m13_complete.data),
            'm14_score': int(self.m14_complete.data),
            'm15_score': int(self.m15_complete.data),
            'penalties': -int(self.penalties_chosen.data)
        }

        score = sum(score_breakdown.values()) if sum(score_breakdown.values()) else 0
        score_breakdown = str(score_breakdown)

        return score, score_breakdown
