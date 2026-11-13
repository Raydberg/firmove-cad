import cadquery as cq

from .parameters import (
    FOREARM_SLOT_POSITIONS,
    FOREARM_CENTRAL_VALVE_D,
    FOREARM_DISTAL_VALVE_D,
    VALVE_THETA_DEG,
)

from .profile import FOREARM_PROFILE
from .shell import create_shell


def create_forearm_module() -> cq.Workplane:
    """
    Carcasa antebraquial en su marco local (+X sale del pivote hacia la
    muneca). Incluye ranuras de ventilacion y los agujeros de paso de
    las valvulas central y distal.
    """

    return create_shell(
        FOREARM_PROFILE,
        slot_positions=FOREARM_SLOT_POSITIONS,
        valve_positions=(
            (FOREARM_CENTRAL_VALVE_D, VALVE_THETA_DEG),
            (FOREARM_DISTAL_VALVE_D, VALVE_THETA_DEG),
        ),
    )
