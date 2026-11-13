import cadquery as cq

from .parameters import (
    FOREARM_ROTATION_DEG,
    STRAP_WIDTH,
    STRAP_THICKNESS,
    STRAP_CLEARANCE,
    BUCKLE_LENGTH,
    BUCKLE_WIDTH,
    BUCKLE_THICKNESS,
    BRAQUIAL_STRAP_POSITIONS,
    FOREARM_STRAP_POSITIONS,
    BRAQUIAL_VALVE_D,
    FOREARM_CENTRAL_VALVE_D,
    FOREARM_DISTAL_VALVE_D,
)

from .profile import BRACHIAL_PROFILE, FOREARM_PROFILE, ShellProfile

from .brachial_module import create_brachial_module
from .forearm_module import create_forearm_module
from .hinge import create_hinge

from .pneumatic import (
    create_brachial_chamber,
    create_central_chamber,
    create_distal_chamber,
    create_brachial_liner,
    create_forearm_liner,
    create_brachial_tube,
    create_central_tube,
    create_distal_tube,
    valve_cylinder,
)


def _strap_ring(profile: ShellProfile, d: float, shrink: float) -> cq.Workplane:

    half = STRAP_WIDTH / 2.0

    return (
        cq.Workplane("YZ")
        .workplane(offset=d - half)
        .ellipse(
            profile.half_width(d - half, shrink),
            profile.half_height(d - half, shrink),
        )
        .workplane(offset=STRAP_WIDTH)
        .ellipse(
            profile.half_width(d + half, shrink),
            profile.half_height(d + half, shrink),
        )
        .loft(ruled=True, combine=True)
    )


def _create_strap(profile: ShellProfile, d: float) -> cq.Workplane:
    """
    Correa que envuelve toda la seccion (carcasa + abertura superior)
    a la distancia d del pivote, con una hebilla en la cara exterior.
    """

    ring = _strap_ring(profile, d, -(STRAP_CLEARANCE + STRAP_THICKNESS)).cut(
        _strap_ring(profile, d, -STRAP_CLEARANCE)
    )

    # Cota exterior de la correa en el centro de la cara lateral
    z_outer = -(profile.half_height(d) + STRAP_CLEARANCE + STRAP_THICKNESS)

    # La hebilla penetra 1.2 mm en la correa para asegurar el contacto
    # incluso donde la seccion se curva hacia arriba.
    overlap = 1.2

    plate = cq.Workplane("XY").box(
        BUCKLE_LENGTH,
        BUCKLE_WIDTH,
        BUCKLE_THICKNESS,
        centered=(True, True, False),
    )

    window = cq.Workplane("XY").box(
        BUCKLE_LENGTH * 0.38,
        BUCKLE_WIDTH * 0.62,
        BUCKLE_THICKNESS + 2.0,
        centered=(True, True, True),
    ).translate((0, 0, BUCKLE_THICKNESS / 2.0))

    buckle = plate.cut(window).translate(
        (d, 0, z_outer - BUCKLE_THICKNESS + overlap)
    )

    return ring.union(buckle)


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

    assy.add(
        create_brachial_module(),
        name="MODULO_BRAQUIAL_01",
        loc=brachial_loc,
        color=cq.Color(0.80, 0.80, 0.80),
    )

    assy.add(
        create_forearm_module(),
        name="MODULO_ANTEBRAQUIAL_02",
        loc=forearm_loc,
        color=cq.Color(0.82, 0.82, 0.82),
    )

    # -------------------------------------------------------
    # Bisagra (centrada en el eje de flexion, sin transformacion)
    # -------------------------------------------------------

    assy.add(
        create_hinge(),
        name="BISAGRA_VISUAL_03",
        color=cq.Color(0.45, 0.45, 0.45),
    )

    # -------------------------------------------------------
    # Correas del modulo braquial
    # -------------------------------------------------------

    for index, d in enumerate(BRAQUIAL_STRAP_POSITIONS, start=1):

        assy.add(
            _create_strap(BRACHIAL_PROFILE, d),
            name=f"CORREA_BRAQUIAL_{index}_10",
            loc=brachial_loc,
            color=cq.Color(0.18, 0.18, 0.18),
        )

    # -------------------------------------------------------
    # Correas del antebrazo
    # -------------------------------------------------------

    for index, d in enumerate(FOREARM_STRAP_POSITIONS, start=1):

        assy.add(
            _create_strap(FOREARM_PROFILE, d),
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
    # Tubos (sobre la pared interior de cada carcasa)
    # -------------------------------------------------------

    assy.add(
        create_brachial_tube(),
        name="TUBO_PROXIMAL_15",
        loc=brachial_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    assy.add(
        create_central_tube(),
        name="TUBO_CENTRAL_15",
        loc=forearm_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    assy.add(
        create_distal_tube(),
        name="TUBO_DISTAL_15",
        loc=forearm_loc,
        color=cq.Color(0.25, 0.25, 0.25),
    )

    # -------------------------------------------------------
    # Valvulas / pulsadores (en la cara exterior, pasan por la
    # carcasa a traves de un agujero)
    # -------------------------------------------------------

    assy.add(
        valve_cylinder(BRACHIAL_PROFILE, BRAQUIAL_VALVE_D),
        name="VALVULA_PROXIMAL_16_17",
        loc=brachial_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    assy.add(
        valve_cylinder(FOREARM_PROFILE, FOREARM_CENTRAL_VALVE_D),
        name="VALVULA_CENTRAL_16_17",
        loc=forearm_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    assy.add(
        valve_cylinder(FOREARM_PROFILE, FOREARM_DISTAL_VALVE_D),
        name="VALVULA_DISTAL_16_17",
        loc=forearm_loc,
        color=cq.Color(0.30, 0.30, 0.30),
    )

    return assy
