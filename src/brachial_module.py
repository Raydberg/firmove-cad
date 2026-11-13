import cadquery as cq

from .parameters import (
    BRAQUIAL_SLOT_POSITIONS,
    BRAQUIAL_VALVE_D,
    VALVE_THETA_DEG,
)

from .profile import BRACHIAL_PROFILE
from .shell import create_shell


def create_brachial_module() -> cq.Workplane:
    """
    Carcasa braquial en su marco local (+X sale del pivote hacia el
    extremo proximal). Incluye ranuras de ventilacion y el agujero de
    paso de la valvula proximal.
    """

    return create_shell(
        BRACHIAL_PROFILE,
        slot_positions=BRAQUIAL_SLOT_POSITIONS,
        valve_positions=((BRAQUIAL_VALVE_D, VALVE_THETA_DEG),),
    )
