import cadquery as cq

from .parameters import (
    AIR_CHAMBER_THICKNESS,
    TUBE_DIAMETER,
    VALVE_DIAMETER,
    VALVE_LENGTH,
    LINER_THICKNESS,
)


def create_rounded_pad(
    length: float,
    width: float,
    thickness: float,
    x: float,
    z: float,
    radius: float = 5.0,
) -> cq.Workplane:

    pad = (
        cq.Workplane("XY")
        .box(
            length,
            width,
            thickness,
            centered=(False, True, True),
        )
        .translate((x, 0, z))
    )

    # Fillet solo en las aristas verticales.
    try:
        pad = pad.edges("|Z").fillet(radius)
    except Exception:
        # Si OpenCascade no puede aplicar el fillet,
        # conservamos la geometria valida.
        pass

    return pad


def create_brachial_chamber() -> cq.Workplane:

    return create_rounded_pad(
        length=72.0,
        width=44.0,
        thickness=AIR_CHAMBER_THICKNESS,
        x=38.0,
        z=-20.0,
        radius=6.0,
    )


def create_central_chamber() -> cq.Workplane:

    return create_rounded_pad(
        length=65.0,
        width=42.0,
        thickness=AIR_CHAMBER_THICKNESS,
        x=22.0,
        z=-18.0,
        radius=6.0,
    )


def create_distal_chamber() -> cq.Workplane:

    return create_rounded_pad(
        length=60.0,
        width=32.0,
        thickness=AIR_CHAMBER_THICKNESS,
        x=110.0,
        z=-15.0,
        radius=6.0,
    )


def create_brachial_liner() -> cq.Workplane:

    return create_rounded_pad(
        length=120.0,
        width=52.0,
        thickness=LINER_THICKNESS,
        x=15.0,
        z=-26.0,
        radius=5.0,
    )


def create_forearm_liner() -> cq.Workplane:

    return create_rounded_pad(
        length=165.0,
        width=44.0,
        thickness=LINER_THICKNESS,
        x=10.0,
        z=-22.0,
        radius=5.0,
    )


def create_tube_x(
    length: float,
    x: float,
    y: float,
    z: float,
) -> cq.Workplane:

    return (
        cq.Workplane("YZ")
        .circle(TUBE_DIAMETER / 2.0)
        .extrude(length)
        .translate((x, y, z))
    )


def create_valve_y(
    x: float,
    y: float,
    z: float,
) -> cq.Workplane:

    return (
        cq.Workplane("XZ")
        .circle(VALVE_DIAMETER / 2.0)
        .extrude(VALVE_LENGTH)
        .translate((x, y, z))
    )