import cadquery as cq

from .parameters import (
    BRAQUIAL_LENGTH,
    BRAQUIAL_WIDTH_ELBOW,
    FOREARM_WIDTH_ELBOW,
    FOREARM_ROTATION_DEG,
    STRAP_WIDTH,
    STRAP_THICKNESS,
)

from .brachial_module import create_brachial_module
from .forearm_module import create_forearm_module
from .hinge import create_hinge

from .pneumatic import (
    create_brachial_chamber,
    create_central_chamber,
    create_distal_chamber,
    create_brachial_liner,
    create_forearm_liner,
    create_tube_x,
    create_valve_y,
)


def _create_strap(
    x: float,
    module_width: float,
) -> cq.Workplane:

    return (
        cq.Workplane("XY")
        .box(
            STRAP_WIDTH,
            module_width + 12.0,
            STRAP_THICKNESS,
            centered=(True, True, False),
        )
        .translate((x, 0, 0.5))
    )


def create_firmove_assembly() -> cq.Assembly:

    assy = cq.Assembly(name="FIRMOVE_ASSEMBLY")

    # -------------------------------------------------------
    # Transformaciones principales
    # -------------------------------------------------------

    # El modulo braquial sale del codo hacia -X.
    brachial_loc = cq.Location(
        (0, 0, 0),
        (0, 0, 1),
        180.0,
    )

    # El antebrazo sale desde el codo formando 125° internos.
    forearm_loc = cq.Location(
        (0, 0, 0),
        (0, 0, 1),
        FOREARM_ROTATION_DEG,
    )

    # -------------------------------------------------------
    # Carcasas principales
    # -------------------------------------------------------

    brachial = create_brachial_module()

    forearm = create_forearm_module()

    assy.add(
        brachial,
        name="MODULO_BRAQUIAL_01",
        loc=brachial_loc,
        color=cq.Color(0.80, 0.80, 0.80),
    )

    assy.add(
        forearm,
        name="MODULO_ANTEBRAQUIAL_02",
        loc=forearm_loc,
        color=cq.Color(0.82, 0.82, 0.82),
    )

    # -------------------------------------------------------
    # Bisagra
    # -------------------------------------------------------

    hinge = create_hinge()

    assy.add(
        hinge,
        name="BISAGRA_VISUAL_03",
        color=cq.Color(0.45, 0.45, 0.45),
    )

    # -------------------------------------------------------
    # Correas del modulo braquial
    # -------------------------------------------------------

    brachial_strap_positions = (
        BRAQUIAL_LENGTH * 0.25,
        BRAQUIAL_LENGTH * 0.70,
    )

    for index, x in enumerate(
        brachial_strap_positions,
        start=1,
    ):

        strap = _create_strap(
            x,
            BRAQUIAL_WIDTH_ELBOW,
        )

        assy.add(
            strap,
            name=f"CORREA_BRAQUIAL_{index}_10",
            loc=brachial_loc,
            color=cq.Color(0.18, 0.18, 0.18),
        )

    # -------------------------------------------------------
    # Correas del antebrazo
    # -------------------------------------------------------

    forearm_strap_positions = (
        45.0,
        115.0,
        165.0,
    )

    for index, x in enumerate(
        forearm_strap_positions,
        start=1,
    ):

        strap = _create_strap(
            x,
            FOREARM_WIDTH_ELBOW,
        )

        assy.add(
            strap,
            name=f"CORREA_ANTEBRAQUIAL_{index}_10",
            loc=forearm_loc,
            color=cq.Color(0.18, 0.18, 0.18),
        )

    # -------------------------------------------------------
    # Camaras neumaticas
    # -------------------------------------------------------

    assy.add(
        create_brachial_chamber(),
        name="CAMARA_PROXIMAL_12",
        loc=brachial_loc,
        color=cq.Color(0.40, 0.65, 0.90),
    )

    assy.add(
        create_central_chamber(),
        name="CAMARA_CENTRAL_13",
        loc=forearm_loc,
        color=cq.Color(0.40, 0.65, 0.90),
    )

    assy.add(
        create_distal_chamber(),
        name="CAMARA_DISTAL_14",
        loc=forearm_loc,
        color=cq.Color(0.40, 0.65, 0.90),
    )

    # -------------------------------------------------------
    # Revestimientos
    # -------------------------------------------------------

    assy.add(
        create_brachial_liner(),
        name="REVESTIMIENTO_BRAQUIAL_18",
        loc=brachial_loc,
        color=cq.Color(0.75, 0.75, 0.55),
    )

    assy.add(
        create_forearm_liner(),
        name="REVESTIMIENTO_ANTEBRAQUIAL_18",
        loc=forearm_loc,
        color=cq.Color(0.75, 0.75, 0.55),
    )

    # -------------------------------------------------------
    # Tubos
    # -------------------------------------------------------

    brachial_tube = create_tube_x(
        length=85.0,
        x=28.0,
        y=-BRAQUIAL_WIDTH_ELBOW / 2.0 + 6.0,
        z=-11.0,
    )

    assy.add(
        brachial_tube,
        name="TUBO_PROXIMAL_15",
        loc=brachial_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    central_tube = create_tube_x(
        length=65.0,
        x=20.0,
        y=-FOREARM_WIDTH_ELBOW / 2.0 + 6.0,
        z=-10.0,
    )

    assy.add(
        central_tube,
        name="TUBO_CENTRAL_15",
        loc=forearm_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    distal_tube = create_tube_x(
        length=60.0,
        x=108.0,
        y=-FOREARM_WIDTH_ELBOW / 2.0 + 7.0,
        z=-9.0,
    )

    assy.add(
        distal_tube,
        name="TUBO_DISTAL_15",
        loc=forearm_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    # -------------------------------------------------------
    # Valvulas / pulsadores simplificados
    # -------------------------------------------------------

    valve_brachial = create_valve_y(
        x=70.0,
        y=-BRAQUIAL_WIDTH_ELBOW / 2.0 - 10.0,
        z=-12.0,
    )

    assy.add(
        valve_brachial,
        name="VALVULA_PROXIMAL_16_17",
        loc=brachial_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    valve_central = create_valve_y(
        x=55.0,
        y=-FOREARM_WIDTH_ELBOW / 2.0 - 10.0,
        z=-11.0,
    )

    assy.add(
        valve_central,
        name="VALVULA_CENTRAL_16_17",
        loc=forearm_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    valve_distal = create_valve_y(
        x=140.0,
        y=-FOREARM_WIDTH_ELBOW / 2.0 - 8.0,
        z=-9.0,
    )

    assy.add(
        valve_distal,
        name="VALVULA_DISTAL_16_17",
        loc=forearm_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    return assy