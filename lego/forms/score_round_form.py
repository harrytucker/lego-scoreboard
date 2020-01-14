# -----------------------------------------------------------------------------
# The form used for scoring the active round.
#
# Needs to be updated each year with the new tasks.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    IntegerField,
    StringField,
    HiddenField,
    RadioField,
    Field,
)
from wtforms import Form, FormField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets import CheckboxInput
import json
import os
from collections import OrderedDict


class ScoredFormField(FormField):
    """ extension to the FormField class to allow the form to generate a score based on the fields it contains """

    def score(self):
        score = 0

        for _, task in self._fields.items():
            if isinstance(task, StringField):
                # strings do not carry any score
                continue
            elif isinstance(task, BooleanField):
                if task.data is False:
                    return 0
            elif isinstance(task, ScoredFormField):
                score += task.score()
            else:
                score += int(task.data)

        return score


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
            return "0"

    def process_formdata(self, valuelist):
        super(CheckboxField, self).process_formdata(valuelist)
        if valuelist:
            self.data = self.value
        else:
            self.data = False


field_classes = {
    "BooleanField": BooleanField,
    "SelectField": SelectField,
    "StringField": StringField,
    "RadioField": RadioField,
    "CheckboxField": CheckboxField,
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

            class_ = field_classes[data["type"]]
            if class_ in (StringField, BooleanField):
                mission[task_no] = class_(data["string"])
            elif class_ == CheckboxField:
                mission[task_no] = class_(data["string"], value=data["value"])
            # abandon all hope ye who enter
            # this little manual exemption here sets the default option for this mission as 6
            # as tokens are taken off the field, not added
            # some browsers would pick the first select option (correct) but some would just
            # select the lowest value as default which caused some issues.
            elif (
                data["string"]
                == "<span>Number of Precision Tokens left on the Field:</span>"
            ):
                mission[task_no] = class_(
                    data["string"],
                    choices=[
                        (choice["value"], choice["string"])
                        for choice in data["choices"]
                    ],
                    default=6,
                    validators=[Optional()],
                )
            #                                -"           ^""**$$$e.
            #                              ."                   '$$$c
            #                             /                      "4$$b
            #                            d  3                      $$$$
            #                            $  *                   .$$$$$$
            #                           .$  ^c           $$$$$e$$$$$$$$.
            #                           d$L  4.         4$$$$$$$$$$$$$$b
            #                           $$$$b ^ceeeee.  4$$ECL.F*$$$$$$$
            #               e$""=.      $$$$P d$$$$F $ $$$$$$$$$- $$$$$$
            #              z$$b. ^c     3$$$F "$$$$b   $"$$$$$$$  $$$$*"      .=""$c
            #             4$$$$L        $$P"  "$$b   .$ $$$$$...e$$        .=  e$$$.
            #             ^*$$$$$c  %..   *c    ..    $$ 3$$$$$$$$$$eF     zP  d$$$$$
            #               "**$$$ec   "   %ce""    $$$  $$$$$$$$$$*    .r" =$$$$P""
            #                     "*$b.  "c  *$e.    *** d$$$$$"L$$    .d"  e$$***"
            #                       ^*$$c ^$c $$$      4J$$$$$% $$$ .e*".eeP"
            #                          "$$$$$$"'$=e....$*$$**$cz$$" "..d$*"
            #                            "*$$$  *=%4.$ L L$ P3$$$F $$$P"
            #                               "$   "%*ebJLzb$e$$$$$b $P"
            #                                 %..      4$$$$$$$$$$ "
            #                                  $$$e   z$$$$$$$$$$%
            #                                   "*$c  "$$$$$$$P"
            #                                    ."""*$$$$$$$$bc
            #                                 .-"    .$***$$$"""*e.
            #                              .-"    .e$"     "*$c  ^*b.
            #                       .=*""""    .e$*"          "*bc  "*$e..
            #                     .$"        .z*"               ^*$e.   "*****e.
            #                     $$ee$c   .d"                     "*$.        3.
            #                     ^*$E")$..$"                         *   .ee==d%
            #                        $.d$$$*                           *  J$$$e*
            #                         """""                              "$$$"

            elif class_ in (RadioField, SelectField):
                mission[task_no] = class_(
                    data["string"],
                    choices=[
                        (choice["value"], choice["string"])
                        for choice in data["choices"]
                    ],
                    default=0,
                    validators=[Optional()],
                )
            else:
                raise TypeError(
                    "The class with the name {} is not defined in the JSON parser".format(
                        data["type"]
                    )
                )
        missions[key] = ScoredFormField(type(key, (Form,), mission))

    # generates FormField containing each missions FormField
    return FormField(type("Missions", (Form,), missions))


class ScoreRoundForm(FlaskForm):
    team = SelectField(
        "Team:", validators=[InputRequired(message="Please select a team.")]
    )
    small_home_zone = BooleanField("Does the robot fit in the small home zone?")
    yellow_card = BooleanField("Yellow card")
    confirm = HiddenField(default="0")
    score = IntegerField("Total score", validators=[Optional()])

    missions = parse_json(os.path.dirname(__file__) + "/../missions.json")

    def points_scored(self) -> (int, str):
        """Calculate the points scored for this round."""
        score_breakdown = OrderedDict()
        bonus = 0
        # protected field '_fields' used due to dynamic generation defining the field names at runtime
        for mission_name, mission in self.missions.form._fields.items():
            score_breakdown[mission_name] = mission.score()
            print(mission.id)
            print(mission.score())
            print(self.small_home_zone.data)
            # successful mission bonus
            if (
                mission.id != "missions-M14 - Precision"
                and mission.score() > 0
                and self.small_home_zone.data is True
            ):
                bonus += 5
            if (
                mission.id == "missions-M02 - Crane (score all that apply)"
                and mission.score() > 0
                and self.small_home_zone.data is True
            ):
                bonus += 5

        # score is the sum of all mission values, with 5 bonus points per successful mission
        # bonus points are only allocated if the robot fits in the smaller maintenance zone
        score = sum(score_breakdown.values()) + bonus

        # ensure score is not less than 0
        if score < 0:
            score = 0
        score_breakdown = str(score_breakdown)

        return score, score_breakdown
