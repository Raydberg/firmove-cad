import math

import cadquery as cq

from .parameters import (
    FOREARM_ROTATION_DEG,
    HINGE_DIAMETER,
    HINGE_THICKNESS,
    HINGE_AXIS_DIAMETER,
    HINGE_SIDE_OFFSET,
    HINGE_Z,
    HINGE_REF_RADIUS,
    HINGE_REF_HOLE_DIAMETER,
    STOP_PIN_DIAMETER,
    STOP_PIN_HEIGHT,
)


def create_hinge() -> cq.Workplane:

    cy = -HINGE_SIDE_OFFSET

    # Disco principal
    disk = (
        cq.Workplane("XY")
        .center(0, cy)
        .circle(HINGE_DIAMETER / 2.0)
        .extrude(HINGE_THICKNESS)
        .translate((0, 0, HINGE_Z))
    )

    # Cuatro posiciones visuales:
    # 0°, 5°, 10°, 15°
    for angle_deg in (0.0, 5.0, 10.0, 15.0):

        angle = math.radians(angle_deg)

        x = HINGE_REF_RADIUS * math.cos(angle)
        y = cy + HINGE_REF_RADIUS * math.sin(angle)

        hole = (
            cq.Workplane("XY")
            .center(x, y)
            .circle(HINGE_REF_HOLE_DIAMETER / 2.0)
            .extrude(HINGE_THICKNESS + 4.0)
            .translate((0, 0, HINGE_Z - 2.0))
        )

        disk = disk.cut(hole)

    # Eje central
    axis = (
        cq.Workplane("XY")
        .center(0, cy)
        .circle(HINGE_AXIS_DIAMETER / 2.0)
        .extrude(HINGE_THICKNESS + 10.0)
        .translate((0, 0, HINGE_Z - 5.0))
    )

    # Placa que conecta hacia el modulo braquial
    brachial_plate = (
        cq.Workplane("XY")
        .box(
            62.0,
            14.0,
            4.0,
            centered=(True, True, True),
        )
        .translate(
            (
                -31.0,
                cy,
                HINGE_Z + HINGE_THICKNESS / 2.0,
            )
        )
    )

    # Placa que conecta hacia el antebrazo
    forearm_plate = (
        cq.Workplane("XY")
        .box(
            62.0,
            14.0,
            4.0,
            centered=(True, True, True),
        )
        .translate(
            (
                31.0,
                cy,
                HINGE_Z + HINGE_THICKNESS / 2.0,
            )
        )
    )

    forearm_plate = forearm_plate.rotate(
        (0, cy, 0),
        (0, cy, 1),
        FOREARM_ROTATION_DEG,
    )

    hinge = (
        disk
        .union(axis)
        .union(brachial_plate)
        .union(forearm_plate)
    )

    # Dos pernos visuales en extremos de regulación
    for angle_deg in (0.0, 15.0):

        angle = math.radians(angle_deg)

        x = HINGE_REF_RADIUS * math.cos(angle)
        y = cy + HINGE_REF_RADIUS * math.sin(angle)

        pin = (
            cq.Workplane("XY")
            .center(x, y)
            .circle(STOP_PIN_DIAMETER / 2.0)
            .extrude(STOP_PIN_HEIGHT)
            .translate(
                (
                    0,
                    0,
                    HINGE_Z - 2.0,
                )
            )
        )

        hinge = hinge.union(pin)

    return hinge