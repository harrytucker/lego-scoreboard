# -----------------------------------------------------------------------------
# The form used for scoring the active round.
#
# Needs to be updated each year with the new tasks.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import RadioField, BooleanField, SelectField, IntegerField, HiddenField, Form, FormField, FieldList
from wtforms.compat import text_type
from wtforms.validators import InputRequired, Optional
import json
from collections import OrderedDict


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


class ScoredForm(Form):
    def score(self):
        score = 0

        for _, task in self._fields.items():
            if isinstance(task, BonusField):                
                score += task.data * int(task.value)
            elif isinstance(task, BooleanField) and task.data is False:
                return 0
            else:
                score += int(task.data)

        return score


class FormManager:

    def new_form(self, name, bases, dict):
        return FieldList(FormField(type(name, bases, dict)), min_entries=1)

    def parse_json(self, path):
        json_data = json.load(open(path))
        missions = OrderedDict()
        for key, mission_data in sorted(json_data.items()):
            mission = OrderedDict()
            for task_no, data in enumerate(mission_data):
                task_no = str(task_no)
                if data['type'] == 'String':
                    mission['label'] = data['string']
                elif data['type'] == 'BooleanField':
                    mission[task_no] = globals()[data['type']](data['string'])
                elif data['type'] == 'BonusField':
                    mission[task_no] = globals()[data['type']](data['string'],
                                                               value=data['value'])
                else:
                    mission[task_no] = globals()[data['type']](data['string'],
                                                               choices=[(choice['value'], choice['string'])
                                                                        for choice in data['choices']],
                                                               default=0,
                                                               validators=[Optional()])
            missions[key] = self.new_form(str(task_no), (ScoredForm,), mission)
        return self.new_form('Missions', (Form,), missions)


form_manager = FormManager()


class ScoreRoundForm(FlaskForm):
    # fields
    team = SelectField('Team:', validators=[InputRequired(message='Please select a team.')])
    yellow_card = BooleanField('Yellow card')
    confirm = HiddenField(default=0)
    score = IntegerField('Total score', validators=[Optional()])

    missions = form_manager.parse_json('missions.json')

    def points_scored(self) -> (int, str):
        """Calculate the points scored for this round."""
        score_breakdown = {}

        for mission_name, mission in self.missions.entries[0].form._fields.items():
            score_breakdown[mission_name] = mission.entries[0].form.score()

        score = sum(score_breakdown.values()) if sum(score_breakdown.values()) else 0
        score_breakdown = str(score_breakdown)

        return score, score_breakdown
