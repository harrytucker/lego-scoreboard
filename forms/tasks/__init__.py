# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

import re

from lego.forms.tasks.shark_shipment_form import SharkShipmentForm
from lego.forms.tasks.service_dog_action_form import ServiceDogActionForm
from lego.forms.tasks.animal_conservation_form import AnimalConservationForm

TASK_FORMS = (
    SharkShipmentForm,
    ServiceDogActionForm,
    AnimalConservationForm
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
