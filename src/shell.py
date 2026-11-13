"""
Constructor comun de carcasas tipo canal para los modulos braquial y
antebraquial (antes duplicado en cada modulo).
"""

import cadquery as cq

from .parameters import (
    SHELL_OPENING_Z,
    SHELL_RIM_FILLET,
    SHELL_END_RADIUS_ELBOW,
    SHELL_END_RADIUS_FREE,
    SLOT_LENGTH,
    SLOT_WIDTH,
    VALVE_HOLE_CLEARANCE,
)

from .profile import ShellProfile
from .pneumatic import valve_cylinder


def _elliptic_loft(profile: ShellProfile, shrink: float) -> cq.Workplane:

    return (
        cq.Workplane("YZ")
        .workplane(offset=profile.d0)
        .ellipse(
            profile.half_width(profile.d0, shrink),
            profile.half_height(profile.d0, shrink),
        )
        .workplane(offset=profile.length)
        .ellipse(
            profile.half_width(profile.d1, shrink),
            profile.half_height(profile.d1, shrink),
        )
        .loft(ruled=True, combine=True)
    )


def _planform(profile: ShellProfile) -> cq.Workplane:
    """
    Silueta en planta (XY) con los extremos redondeados. Se extruye en
    Z y se intersecta con la carcasa para suavizar sus extremos.
    """

    a0 = profile.half_width(profile.d0)
    a1 = profile.half_width(profile.d1)

    plan = (
        cq.Workplane("XY")
        .workplane(offset=-100.0)
        .polyline(
            [
                (profile.d0, -a0),
                (profile.d1, -a1),
                (profile.d1, a1),
                (profile.d0, a0),
            ]
        )
        .close()
        .extrude(200.0)
    )

    try:
        plan = plan.edges("|Z").edges("<X").fillet(SHELL_END_RADIUS_ELBOW)
        plan = plan.edges("|Z").edges(">X").fillet(SHELL_END_RADIUS_FREE)
    except Exception:
        pass

    return plan


def _round_rim(shell: cq.Workplane, profile: ShellProfile) -> cq.Workplane:
    """
    Redondea solo las aristas largas del canto de la abertura. Incluir
    las aristas cortas de los extremos produce un solido invalido, asi
    que se descarta cualquier filete que no deje la pieza valida.
    """

    rim = [
        e
        for e in shell.edges(">Z").vals()
        if e.BoundingBox().xlen > 0.5 * profile.length
    ]

    if not rim:
        return shell

    try:
        rounded = shell.newObject(rim).fillet(SHELL_RIM_FILLET)
    except Exception:
        return shell

    return rounded if rounded.val().isValid() else shell


def create_shell(
    profile: ShellProfile,
    slot_positions: tuple,
    valve_positions: tuple = (),
) -> cq.Workplane:
    """
    Carcasa hueca abierta hacia +Z.

    - La abertura se corta por encima del ecuador (envuelve > 180 grados).
    - Extremos redondeados en planta y borde de la abertura redondeado.
    - Ranuras de ventilacion en la cara exterior (-Z), posiciones en d.
    - Agujeros de paso para las valvulas (d, theta).
    """

    shell = _elliptic_loft(profile, 0.0).cut(
        _elliptic_loft(profile, profile.thickness)
    )

    max_width = max(profile.width0, profile.width1)
    max_height = max(profile.height0, profile.height1)

    opening_cut = (
        cq.Workplane("XY")
        .box(
            profile.length + 20.0,
            max_width + 20.0,
            max_height,
            centered=(True, True, False),
        )
        .translate(((profile.d0 + profile.d1) / 2.0, 0, SHELL_OPENING_Z))
    )

    shell = shell.cut(opening_cut)

    # Primero el canto y despues el redondeo en planta: al reves, el
    # filete se encuentra con los arcos de los extremos y falla.
    shell = _round_rim(shell, profile)

    shell = shell.intersect(_planform(profile))

    # Ranuras de ventilacion
    for d in slot_positions:
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=-max_height - 10.0)
            .center(d, 0)
            .slot2D(SLOT_LENGTH, SLOT_WIDTH)
            .extrude(max_height + 10.0)
        )
        shell = shell.cut(cutter)

    # Agujeros de las valvulas
    for d, theta in valve_positions:
        shell = shell.cut(
            valve_cylinder(profile, d, theta, clearance=VALVE_HOLE_CLEARANCE)
        )

    return shell
