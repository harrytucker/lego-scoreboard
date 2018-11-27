# -----------------------------------------------------------------------------
# The form used for scoring the active round.
#
# Needs to be updated each year with the new tasks.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import RadioField, BooleanField, SelectField, IntegerField, HiddenField, Form, FormField, FieldList
from wtforms.compat import text_type
from wtforms.validators import InputRequired, Optional


# A boolean field (checkbox) with an associated non-bool value (e.g. an int) 
# class CheckboxValueField(BooleanField):
#     def __init__(self, label=None, validators=None, false_values=None, value=None, **kwargs):
#         super(CheckboxValueField, self).__init__(label, validators, false_values, **kwargs)
#         self.value = value


#     def _value(self):
#         if self.raw_data:
#             return text_type(self.raw_data[0])

#         if self.value:
#             return self.value

#         return 'y'
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

# used to combine several checkbox field values into one object
class CompleteField():
    def __init__(self, components, label):
        self.components = components
        self.data = 0
        for component in components:
            # if the checkbox is a scoring one add its value to the total
            if isinstance(component.value, int):
                self.data += component.value
            # if its an essential condition that wasn't met, set it to 0
            elif isinstance(component.value, bool):
                if component.value == False:
                    self.data = 0
                    break
            
        self.label = label


class ScoredField:
    def score(self):
        score = 0

        for _, task in self._fields.items():
            if isinstance(task, BonusField):
                score += task.data * int(task.value)
            else:
                score += int(task.data)

        return score


class FormManager:
    def __init__(self):
        self.forms = {}

    def new_form(self, name, bases, dict):
        if name not in self.forms:
            self.forms[name] = FieldList(FormField(type(name, bases, dict)), min_entries=1)
        return self.forms[name]


form_manager = FormManager()


class ScoreRoundForm(FlaskForm):
    # fields
    team = SelectField('Team:', validators=[InputRequired(message='Please select a team.')])
    yellow_card = BooleanField('Yellow card')
    confirm = HiddenField(default=0)
    score = IntegerField('Total score', validators=[Optional()])

    missions = form_manager.new_form('Missions', (Form,), {
        'M01 - Space Travel': form_manager.new_form('M01', (Form, ScoredField), {
            'label': 'Send Payload rockets (carts) down the Space Travel Ramp.',
            'm01_independent': BonusField('Cart was independent by the time it made the first track connection',
                                          value='99999'),
            'm01_crew': BonusField('Crew Payload', value='10'),
            'm01_supply': BonusField('Supply payload', value='14'),
            'm01_vehicle': BonusField('Vehicle payload', value='22')
        }),
        'M02 - Solar Panel Array': form_manager.new_form('M02', (Form, ScoredField), {
            'label' : '1',
            'solar_panels': RadioField('Solar Panels need to be angled toward or away from you, depending on strategy and conditions.',
                                       choices=[('18', 'Your Solar Panel is Angled toward the other team’s field'),
                                                ('22', 'Both Solar Panels are angled towards the same field')],
                                       default=0,
                                       validators=[Optional()]
                                       )
        }),
        'M03 - 3D Printing': form_manager.new_form('M03', (Form, ScoredField), {
            'label': 'The Regolith Core must be placed into the 3D Printer, the ejected 2x4 Brick can be delivered for more points.',
            'm03_ejected': BonusField('2x4 Brick completely ejected from the printer by placing a Regolith Core Sample into it', value='18'),
            'm03_planet_area': BonusField('Brick completely in Northeast Planet Area ', value='4')
        }),
        'M04 - Crater Crossing': form_manager.new_form('M04', (Form, ScoredField), {
            'label': 'The Robot or whatever agent-craft it sends out needs to cross the Craters Model, by driving directly over it.',
            'm04_crossed': BonusField('Robot or Agent crossed completely east to west between the towers', value='99999'),
            'm04_gate': BonusField('Gate completely flattened', value='20')
        }),
        'M05 - Extraction': form_manager.new_form('M05', (Form, ScoredField), {
            'label': 'The Robot must get all the Core Samples out of the Core Site.',
            'm05_all_samples': BonusField('All samples moved no longer touching Core Site Model Axis', value='16'),
            'm05_gas_core_touching': BonusField('Gas Core Sample touching the mat and completely in the Lander’s Target Circle', value='12'),
            'm05_gas_core_completely': BonusField('Gas Core Sample completely in Base', value='12'),
            'm05_water_core': BonusField('Water Core Sample supported only by the Food Growth Chamber', value='12')
        }),
        'M06 - Space Station Modules': form_manager.new_form('M06', (Form, ScoredField), {
            'label': 'The Robot needs to remove and insert Modules among the Habitation Hub port holes.',
            'm06_completely': BonusField('Cone Module completely in base', value='16'),
            'm06_tube': BonusField('Tube Module in Habitation Hub Port West Side, touching nothing but the Habitation Hub', value='16'),
            'm06_docking': BonusField('Docking Module in Habitation Hub Port East Side, touching nothing but the Habitation Hub', value='14'),
        }),
        'M07 - Space Walk Emergency': form_manager.new_form('M07', (Form, ScoredField), {
            'label': '2',
            'gerhard': RadioField('The Robot needs to get Gerhard’s body into the Airlock Chamber.',
                                  choices=[('0', 'Gerhard’s body not in airlock chamber'),
                                           ('18', 'Gerhard’s body partially in airlock chamber'),
                                           ('22', 'Gerhard’s body completely in airlock chamber')],
                                  validators=[InputRequired('Please make a choice for M07')])
        }),
        'M08 - Aerobic Exercise': form_manager.new_form('M08', (Form, ScoredField), {
            'label': '3',
            'exercise_machine': SelectField('The Robot needs to repeatedly move one or both of the Exercise Machine’s Handle Assemblies to make the Pointer advance.',
                                            # TODO the first choice must be checked for the others to count
                                            #  Make this a checkbox
                                            choices=[('0', 'Exercise Machine Pointer advanced only by moving one or both of the Handle Assemblies'),
                                                     # Make these an unlocked radio choice if above checkbox is ticked
                                                     ('18', 'Pointer completely in gray, or partly covering either of gray’s end-borders'),
                                                     ('20', 'Pointer completely in white'),
                                                     ('22', 'Pointer completely in orange, or partly covering either of orange’s end-borders')],
                                            default=0,
                                            validators=[Optional()])
        }),
        'M09 - Strength Exercise': form_manager.new_form('M09', (Form, ScoredField), {
            'label': '4',
            'strength_bar': RadioField('The Robot lifted the Strength Bar to a scoring height so that the tooth-strip’s 4th hole comes at least partly into view?',
                                      choices=[('16', 'Yes'),
                                               ('0', 'No')],
                                      default=0,
                                      validators=[InputRequired('Please make a choice for M09')])
        }),
        'M10 - Food Production': form_manager.new_form('M10', (Form, ScoredField), {
            'label': '5',
            'growth_chamber': RadioField('Food Growth Chamber’s colors spun, by moving the Push Bar, so the gray weight is DROPPED after green, but before tan?',
                                         choices=[('16', 'Yes'),
                                                 ('0', 'No')],
                                         default=0,
                                         validators=[InputRequired('Please make a choice for M10')])
        }),
        'M11 - Escape Velocity': form_manager.new_form('M11', (Form, ScoredField), {
            'label': '6',
            'strike_pad': RadioField('The Robot hit the Strike Pad hard enough to keep the spacecraft from dropping back down?',
                                     choices=[('24', 'Yes'),
                                              ('0', 'No')],
                                     default=0,
                                     validators=[InputRequired('Please make a choice for M11')])
        }),
        'M12 - Satellite Orbits': form_manager.new_form('M12', (Form, ScoredField), {
            'label': '7',
            'satellites': RadioField('The Robot needs to move one or more Satellites to the Outer Orbit.',
                                     choices=[('0', 'No satellites moved into orbit'),
                                              ('8', '1 moved between the two lines of the Outer Orbit'),
                                              ('16', '2 moved between the two lines of the Outer Orbit'),
                                              ('24', '3 moved between the two lines of the Outer Orbit')],
                                     default=0,
                                     validators=[InputRequired('Please make a choice for M12')])
        }),
        'M13 - Observatory': form_manager.new_form('M13', (Form, ScoredField), {
            'label': '8',
            'observatory': RadioField('Rotate the Observatory to a precise direction.',
                                      choices=[('0', 'Tip not in any coloured section'),
                                               ('16', 'Tip completely in gray, or partly covering either of gray’s end-borders'),
                                               ('18', 'Tip completely in white'),
                                               ('20', 'Tip completely in orange, or partly covering either of orange’s end-borders')],
                                      default=0,
                                      validators=[InputRequired('Please make a choice for M13')])
        }),
        'M14 - Meteoroid Deflection': form_manager.new_form('M14', (Form, ScoredField), {
            'label': '9',
            'meteoroid': SelectField('Send Meteoroids over the Free-Line to touch the mat in the Meteoroid Catcher.',
                                     # TODO this conditional
                                     choices=[
                                         (True, 'Meteoroids hit/released while clearly and completely west of free line'),
                                         (True, 'Meteoroids clearly independent whilst west of the free-line'),
                                         # TODO two dropdowns for side and center
                                         #  validate with side + centre <= 2
                                         ('12', 'One meteoroid in the Center Section'),
                                         ('24', 'Two meteoroids in the Center Section'),
                                         ('8', 'One in Side section'),
                                         ('16', 'Both in Side section(s)'),
                                         ('20', 'Side and Center')],
                                     default=0,
                                     validators=[InputRequired('Please make a choice for M14')])
        }),
        'M15 - Landing Touch-Down': form_manager.new_form('M15', (Form, ScoredField), {
            'label': '10',
            'lander': RadioField('Get the Lander to one of its targets intact, or at least get it to Base.',
                                 choices=[('0', 'Failed to get lander to target or base'),
                                          ('16', 'Both parts of the Lander completely into Base'),
                                          ('20', 'Lander  intact, touching the Mat, and completely in the Northeast Planet Area'),
                                          ('22', 'Lander intact, touching the Mat, and completely in its Target Circle')],
                                 default=0,
                                 validators=[InputRequired('Please make a choice for M15')])
        }),
        'Penalties': form_manager.new_form('P', (Form, ScoredField), {
            'label': '11',
            'penalties': SelectField('Number of penalties',
                                    choices=[('0', '0'),
                                             ('-3', '1 (-3 points)'),
                                             ('-6', '2 (-6 points)'),
                                             ('-9', '3 (-9 points)'),
                                             ('-12', '4 (-12 points)'),
                                             ('-15', '5 (-15 points)'),
                                             ('-18', '6 (-18 points)')],
                                    default=0,
                                    validators=[Optional()])
        })
    })


    def points_scored(self) -> (int, str):
        """Calculate the points scored for this round."""
        score_breakdown = {}

        for mission_name, mission in self.missions.entries[0].form._fields.items():
            score_breakdown[mission_name] = mission.entries[0].form.score()

        score = sum(score_breakdown.values()) if sum(score_breakdown.values()) else 0
        score_breakdown = str(score_breakdown)

        return score, score_breakdown
