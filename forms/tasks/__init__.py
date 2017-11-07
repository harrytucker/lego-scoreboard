# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------

import re

# tasks M01-M18 in order
from lego.forms.tasks.m01_pipe_removal_form import M01PipeRemovalForm
from lego.forms.tasks.m02_flow_form import M02FlowForm
from lego.forms.tasks.m03_pump_addition_form import M03PumpAdditionForm
from lego.forms.tasks.m04_rain_form import M04RainForm
from lego.forms.tasks.m05_filter_form import M05FilterForm
from lego.forms.tasks.m06_water_treatment_form import M06WaterTreatmentForm
from lego.forms.tasks.m07_fountain_form import M07FountainForm
from lego.forms.tasks.m08_manhole_covers_form import M08ManholeCoversForm
from lego.forms.tasks.m09_tripod_form import M09TripodForm
from lego.forms.tasks.m10_pipe_replacement_form import M10PipeReplacementForm
from lego.forms.tasks.m11_pipe_construction_form import M11PipeConstructionForm
from lego.forms.tasks.m12_sludge_form import M12SludgeForm
from lego.forms.tasks.m13_flower_form import M13FlowerForm
from lego.forms.tasks.m14_water_well_form import M14WaterWellForm
from lego.forms.tasks.m15_fire_form import M15FireForm
from lego.forms.tasks.m16_water_collection_form import M16WaterCollectionForm
from lego.forms.tasks.m17_slingshot_form import M17SlingshotForm
from lego.forms.tasks.m18_faucet_form import M18FaucetForm


TASK_FORMS = (
    M01PipeRemovalForm,
    M02FlowForm,
    M03PumpAdditionForm,
    M04RainForm,
    M05FilterForm,
    M06WaterTreatmentForm,
    M07FountainForm,
    M08ManholeCoversForm,
    M09TripodForm,
    M10PipeReplacementForm,
    M11PipeConstructionForm,
    M12SludgeForm,
    M13FlowerForm,
    M14WaterWellForm,
    M15FireForm,
    M16WaterCollectionForm,
    M17SlingshotForm,
    M18FaucetForm,
)

def form_to_template(form_cls) -> str:
    """..."""

    def replacement(match):
        """..."""
        return '_' + match.group(1).lower()

    # remove form suffix
    template = form_cls.__class__.__name__.replace('Form', '')
    # convert upper camel case to snake case
    template = re.sub(r'([A-Z])', replacement, template)
    # remove leading underscore left over from previous step
    template = template[1:]

    return template
