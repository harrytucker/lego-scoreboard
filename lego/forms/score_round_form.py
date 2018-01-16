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
    m01_title = 'M01 - Pipe Removal'
    m02_title = 'M02 - Flow'
    m03_title = 'M03 - Pump Addition'
    m04_title = 'M04 - Rain'
    m05_title = 'M05 - Filter'
    m06_title = 'M06 - Water Treatment'
    m07_title = 'M07 - Fountain'
    m08_title = 'M08 - Manhole Covers'
    m09_title = 'M09 - Tripod'
    m10_title = 'M10 - Pipe Replacement'
    m11_title = 'M11 - Pipe Construction'
    m12_title = 'M12 - Sludge'
    m13_title = 'M13 - Flower'
    m14_title = 'M14 - Water Well'
    m15_title = 'M15 - Fire'
    m16_title = 'M16 - Water Collection'
    m17_title = 'M17 - Slingshot'
    m18_title = 'M18 - Faucet'
    penalties_title = 'Penalties'

    # fields
    team = SelectField('Team:', validators=[InputRequired(message='Please select a team.')])
    yellow_card = BooleanField('Yellow card')
    confirm = HiddenField(default='0')
    score = IntegerField('Total score', validators=[Optional()])

    m01_complete = RadioField('Broken Pipe completely in Base.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M01.')])

    m02_complete = RadioField('Big Water in other teams field, achieved by only turning the '
                              'Pump system valves.',
                              choices=[('25', 'Yes (25 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M02.')])

    m03_complete = RadioField('Pump Addition is in contact with the mat and is completely in the '
                              'Pump Addition target.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M03')])

    m04_complete = RadioField('At least one Rain out of the Rain Cloud.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M04')])

    m05_complete = RadioField('Filter moved north until the lock latch dropped.',
                              choices=[('30', 'Yes (30 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M05')])

    m06_complete = RadioField('Big Water ejected from Water Treatment, only by moving the '
                              'Toilet lever.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M06')])

    m07_complete = RadioField('Fountain middle layer raised some obvious amount, only due to a '
                              'Big Water in the gray tub.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M07')])

    m08_complete = SelectField('Manhole covers flipped past vertical.',
                               choices=[('0', '0 (0 points)'),
                                        ('15', '1 (15 points)'),
                                        ('30', '2 (30 points)')],
                               validators=[Optional()])
    m08_bonus = BonusField('Both covers completely in separate Tripod target areas (30 points).',
                           value='30')

    m09_complete = SelectField('Tripod in either Tripod target, with all of its feet touching the '
                               'mat.',
                               choices=[('0', 'Not in target (0 points)'),
                                        ('15', 'Partially in target (15 points)'),
                                        ('20', 'Completely in target (20 points)')],
                               validators=[Optional()])

    m10_complete = RadioField('New Pipe where broken pipe started, in full/flat contact with '
                              'the mat.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M10')])

    m11_complete = SelectField('New Pipe in the target and in full/flat contact ' \
                               'with the mat.',
                               choices=[('0', 'Not in target (0 points)'),
                                        ('15', 'Partially in target (15 points)'),
                                        ('20', 'Completely in target (20 points)')],
                               validators=[Optional()])

    m12_complete = RadioField('Sludge touching the visible wood of a garden box.',
                              choices=[('30', 'Yes (30 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M12')])

    m13_complete = RadioField('Flower raise an obvious amount only due to Big Water in the '
                              'brown pot.',
                              choices=[('30', 'Yes (30 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M13')])
    m13_bonus = BonusField('At least one Rain in the purple part not touching anything but the '
                           'flower model (30 points).',
                           value='30')

    m14_complete = SelectField('Water Well in contact with the mat and in the Water Well target.',
                               choices=[('0', 'Not in target (0 points)'),
                                        ('15', 'Partially in target (15 points)'),
                                        ('25', 'Completely in target (25 points)')],
                               validators=[Optional()])

    m15_complete = RadioField('Fire dropped, only y Fireturck applying force to house lever.',
                              choices=[('25', 'Yes (25 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M15')])

    m16_part_1 = RadioField('At least one Rain in Water Collection Area.',
                            choices=[('10', 'Yes (10 points)'),
                                     ('0', 'No (0 points)')],
                            default='0',
                            validators=[InputRequired('Please make a choice for M16')])
    m16_part_2 = SelectField('Big Water in Water Collection Area.',
                             choices=[('0', '0 (0 points)'),
                                      ('10', '1 (10 points)'),
                                      ('20', '2 (20 points)'),
                                      ('30', '3 (30 points)'),
                                      ('40', '4 (40 points)'),
                                      ('50', '5 (50 points)')],
                             validators=[Optional()])
    m16_bonus = BonusField('One scoring Big Water an top of second scoring Big Water, touching '
                           'nothing but other water (30 points).',
                           value='30')

    m17_complete = RadioField('Slingshot completely in its target area.',
                              choices=[('20', 'Yes (20 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M17')])
    m17_bonus = BonusField('Dirty Water and a Rain completely in the target (15 points).',
                           value='15')


    m18_complete = RadioField('Water level more blue than white by only turning Faucet handle.',
                              choices=[('25', 'Yes (25 points)'),
                                       ('0', 'No (0 points)')],
                              default='0',
                              validators=[InputRequired('Please make a choice for M18')])

    penalties_chosen = SelectField('Number of penalties',
                             choices=[('0', '0 (0 points)'),
                                      ('5', '1 (-5 points)'),
                                      ('10', '2 (-10 points)'),
                                      ('15', '3 (-15 points)'),
                                      ('20', '4 (-20 points)'),
                                      ('25', '5 (-25 points)'),
                                      ('30', '6 (-30 points)')],
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
