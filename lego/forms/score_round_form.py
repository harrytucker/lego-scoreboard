# -----------------------------------------------------------------------------
# The form used for scoring the active round.
#
# Needs to be updated each year with the new tasks.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, IntegerField, StringField, HiddenField, RadioField, Field
from wtforms import Form, FormField, FieldList
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import CheckboxInput
import json
import os
from collections import OrderedDict


class CheckboxField(Field):

    widget = CheckboxInput()

    def __init__(self, *args, value=None, **kwargs):
        super(CheckboxField, self).__init__(*args, **kwargs)
        self.data = False
        self.value = value

    def _value(self):
        if self.data:
            return self.value
        else:
            return '0'

    def process_formdata(self, valuelist):
        super(CheckboxField, self).process_formdata(valuelist)
        if valuelist:
            self.data = self.value
        else:
            self.data = False


fields = {
    'BooleanField': BooleanField,
    'SelectField': SelectField,
    'StringField': StringField,
    'RadioField': RadioField,
    'CheckboxField': CheckboxField
}


def parse_json(path):
    """ parses json file and generates a FieldList full of FieldLists for all the missions """
    json_data = json.load(open(path))
    missions = OrderedDict()
    # sorts the json return based on the mission name as json libraries do not preserve order
    for key, mission_data in sorted(json_data.items()):
        mission = OrderedDict()
        for task_no, data in enumerate(mission_data):
            # converts the task_no to a string to avoid a crash
            task_no = str(task_no)
            class_ = fields[data['type']]
            if class_ in (StringField, BooleanField):
                mission[task_no] = class_(data['string'])
            elif class_ == CheckboxField:
                mission[task_no] = class_(data['string'],
                                          value=data['value'])
            elif class_ in (RadioField, SelectField):
                mission[task_no] = class_(data['string'],
                                          choices=[(choice['value'], choice['string'])
                                                   for choice in data['choices']],
                                          default=0,
                                          validators=[Optional()])
            else:
                raise TypeError('The class with the name {} is not defined in the JSON parser'.format(data['type']))
        missions[key] = FormField(type(str(task_no), (ScoredForm,), mission))

    # generates FiledList containing each missions FieldList
    return FormField(type('Missions', (Form,), missions))


class ScoredForm(Form):
    """ extension to the Form class to allow the form to generate a score based on the fields it contains """
    def score(self):
        score = 0

        for _, task in self._fields.items():
            if isinstance(task, StringField):
                # strings do not carry any score
                continue
            elif isinstance(task, BooleanField):
                if task.data is False:
                    return 0
            else:
                score += int(task.data)

        return score


class ScoreRoundForm(FlaskForm):
    team = SelectField('Team:', validators=[InputRequired(message='Please select a team.')])
    yellow_card = BooleanField('Yellow card')
    confirm = HiddenField(default='0')
    score = IntegerField('Total score', validators=[Optional()])

    missions = parse_json(os.path.dirname(__file__) + '/../missions.json')

    def points_scored(self) -> (int, str):
        """Calculate the points scored for this round."""
        score_breakdown = {}
        # protected field '_fields' used due to dynamic generation defining the field names at runtime
        for mission_name, mission in self.missions.form._fields.items():
            score_breakdown[mission_name] = mission.form.score()

        score = sum(score_breakdown.values())

        # ensure score is not less than 0
        if score < 0:
            score = 0
        score_breakdown = str(score_breakdown)

        return score, score_breakdown
