import math

import cadquery as cq

from .parameters import (
    FOREARM_ROTATION_DEG,
    HINGE_DIAMETER,
    HINGE_THICKNESS,
    HINGE_AXIS_DIAMETER,
    HINGE_SIDE_OFFSET,
    HINGE_Z,
    HINGE_BAR_THICKNESS,
    HINGE_BAR_LENGTH,
    HINGE_BAR_WIDTH,
    HINGE_HUB_DIAMETER,
    HINGE_HUB_HEIGHT,
    HINGE_REF_RADIUS,
    HINGE_REF_HOLE_DIAMETER,
    STOP_PIN_DIAMETER,
    STOP_PIN_HEIGHT,
)


def _cylinder(x: float, y: float, z_bottom: float, height: float, diameter: float):
    return (
        cq.Workplane("XY")
        .workplane(offset=z_bottom)
        .center(x, y)
        .circle(diameter / 2.0)
        .extrude(height)
    )


def _bar(z_bottom: float) -> cq.Workplane:
    """
    Barra con extremos redondeados que parte del pivote hacia +X
    (el extremo del pivote es concentrico con el eje de giro).
    """

    cap = HINGE_BAR_WIDTH / 2.0
    overall = HINGE_BAR_LENGTH + cap

    return (
        cq.Workplane("XY")
        .workplane(offset=z_bottom)
        .center((HINGE_BAR_LENGTH - cap) / 2.0, 0)
        .slot2D(overall, HINGE_BAR_WIDTH)
        .extrude(HINGE_BAR_THICKNESS)
    )


def _rivets(z_bottom: float, distances=(42.0, 56.0)) -> cq.Workplane:
    """Cabezas de remache sobre la cara exterior (-Z) de una barra."""

    result = None

    for d in distances:
        head = _cylinder(d, 0, z_bottom - 1.2, 1.2, 5.0)
        result = head if result is None else result.union(head)

    return result


def create_hinge() -> cq.Workplane:
    """
    Bisagra visual centrada en el eje de flexion (origen), por fuera de
    las carcasas (lado -Z). Capas desde la carcasa hacia afuera:

        barra antebraquial -> barra braquial -> disco -> cubo

    La barra antebraquial queda en contacto con la cara exterior de la
    carcasa del antebrazo (cota -FOREARM_HEIGHT_ELBOW / 2).
    """

    cy = -HINGE_SIDE_OFFSET

    disk_bottom = HINGE_Z
    disk_top = HINGE_Z + HINGE_THICKNESS

    brachial_bar_bottom = disk_top
    forearm_bar_bottom = brachial_bar_bottom + HINGE_BAR_THICKNESS

    # Disco principal
    disk = _cylinder(0, cy, disk_bottom, HINGE_THICKNESS, HINGE_DIAMETER)

    # Cuatro posiciones visuales de tope: 0, 5, 10 y 15 grados
    # (limite de extension, medido desde la direccion de extension total).
    for angle_deg in (0.0, 5.0, 10.0, 15.0):

        angle = math.radians(angle_deg)

        x = HINGE_REF_RADIUS * math.cos(angle)
        y = cy + HINGE_REF_RADIUS * math.sin(angle)

        hole = _cylinder(
            x,
            y,
            disk_bottom - 1.0,
            HINGE_THICKNESS + 2.0,
            HINGE_REF_HOLE_DIAMETER,
        )

        disk = disk.cut(hole)

    # Cubo exterior
    hub = _cylinder(
        0, cy, disk_bottom - HINGE_HUB_HEIGHT, HINGE_HUB_HEIGHT, HINGE_HUB_DIAMETER
    )

    # Eje central: atraviesa todas las capas
    axis = _cylinder(
        0,
        cy,
        disk_bottom - HINGE_HUB_HEIGHT - 3.0,
        (forearm_bar_bottom + HINGE_BAR_THICKNESS + 2.0)
        - (disk_bottom - HINGE_HUB_HEIGHT - 3.0),
        HINGE_AXIS_DIAMETER,
    )

    # Barra hacia el modulo braquial (sale del pivote hacia -X)
    brachial_bar = _bar(brachial_bar_bottom).rotate((0, 0, 0), (0, 0, 1), 180.0)

    # Barra hacia el antebrazo (sigue la rotacion del antebrazo)
    forearm_bar = _bar(forearm_bar_bottom).rotate(
        (0, 0, 0), (0, 0, 1), FOREARM_ROTATION_DEG
    )

    brachial_rivets = _rivets(brachial_bar_bottom).rotate((0, 0, 0), (0, 0, 1), 180.0)
    forearm_rivets = _rivets(forearm_bar_bottom).rotate(
        (0, 0, 0), (0, 0, 1), FOREARM_ROTATION_DEG
    )

    hinge = (
        disk.union(hub)
        .union(axis)
        .union(brachial_bar)
        .union(forearm_bar)
        .union(brachial_rivets)
        .union(forearm_rivets)
    )

    # Dos pernos de tope (extremos de regulacion): 0 y 15 grados.
    # Atraviesan el disco y sobresalen por la cara exterior.
    for angle_deg in (0.0, 15.0):

        angle = math.radians(angle_deg)

        x = HINGE_REF_RADIUS * math.cos(angle)
        y = cy + HINGE_REF_RADIUS * math.sin(angle)

        pin = _cylinder(
            x,
            y,
            disk_top - STOP_PIN_HEIGHT,
            STOP_PIN_HEIGHT,
            STOP_PIN_DIAMETER,
        )

        hinge = hinge.union(pin)

    return hinge
