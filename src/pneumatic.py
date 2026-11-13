import cadquery as cq

from .parameters import (
    AIR_CHAMBER_THICKNESS,
    TUBE_DIAMETER,
    TUBE_THETA_DEG,
    VALVE_DIAMETER,
    VALVE_LENGTH,
    VALVE_THETA_DEG,
    LINER_THICKNESS,
)

from .profile import BRACHIAL_PROFILE, FOREARM_PROFILE, ShellProfile


# ------------------------------------------------------------
# Pads conformados a la pared interior de la carcasa
# ------------------------------------------------------------


def _slab(profile: ShellProfile, d0: float, d1: float, shrink: float):
    """Loft reglado de la elipse de la carcasa reducida en `shrink`."""

    a0, b0 = profile.half_width(d0, shrink), profile.half_height(d0, shrink)
    a1, b1 = profile.half_width(d1, shrink), profile.half_height(d1, shrink)

    return (
        cq.Workplane("YZ")
        .workplane(offset=d0)
        .ellipse(a0, b0)
        .workplane(offset=d1 - d0)
        .ellipse(a1, b1)
        .loft(ruled=True, combine=True)
    )


def create_conformal_pad(
    profile: ShellProfile,
    s_start: float,
    length: float,
    width: float,
    thickness: float,
    inset: float,
    radius: float,
) -> cq.Workplane:
    """
    Pad curvo que sigue la pared interior de la carcasa.

    s_start: distancia desde el inicio de la carcasa.
    inset:   separacion entre la pared interior y la cara exterior del pad.
    """

    d0 = profile.d0 + s_start
    d1 = d0 + length

    outer_shrink = profile.thickness + inset
    inner_shrink = outer_shrink + thickness

    band = _slab(profile, d0, d1, outer_shrink).cut(
        _slab(profile, d0, d1, inner_shrink)
    )

    footprint = (
        cq.Workplane("XY")
        .workplane(offset=-100.0)
        .center((d0 + d1) / 2.0, 0)
        .rect(length, width)
        .extrude(100.0)
    )

    try:
        footprint = footprint.edges("|Z").fillet(radius)
    except Exception:
        pass

    return band.intersect(footprint)


# Orden de capas desde la pared hacia la piel:
#   pared de la carcasa -> revestimiento -> camara neumatica


def create_brachial_liner() -> cq.Workplane:
    return create_conformal_pad(
        BRACHIAL_PROFILE,
        s_start=15.0,
        length=120.0,
        width=52.0,
        thickness=LINER_THICKNESS,
        inset=0.0,
        radius=5.0,
    )


def create_forearm_liner() -> cq.Workplane:
    return create_conformal_pad(
        FOREARM_PROFILE,
        s_start=10.0,
        length=165.0,
        width=44.0,
        thickness=LINER_THICKNESS,
        inset=0.0,
        radius=5.0,
    )


def create_brachial_chamber() -> cq.Workplane:
    return create_conformal_pad(
        BRACHIAL_PROFILE,
        s_start=38.0,
        length=72.0,
        width=44.0,
        thickness=AIR_CHAMBER_THICKNESS,
        inset=LINER_THICKNESS,
        radius=6.0,
    )


def create_central_chamber() -> cq.Workplane:
    return create_conformal_pad(
        FOREARM_PROFILE,
        s_start=22.0,
        length=65.0,
        width=42.0,
        thickness=AIR_CHAMBER_THICKNESS,
        inset=LINER_THICKNESS,
        radius=6.0,
    )


def create_distal_chamber() -> cq.Workplane:
    return create_conformal_pad(
        FOREARM_PROFILE,
        s_start=110.0,
        length=60.0,
        width=32.0,
        thickness=AIR_CHAMBER_THICKNESS,
        inset=LINER_THICKNESS,
        radius=6.0,
    )


# ------------------------------------------------------------
# Tubos: rectas sobre la pared interior (theta constante)
# ------------------------------------------------------------


def create_tube(
    profile: ShellProfile,
    d_start: float,
    d_end: float,
    theta_deg: float = TUBE_THETA_DEG,
) -> cq.Workplane:

    r = TUBE_DIAMETER / 2.0
    pts = []

    for d in (d_start, d_end):
        # Centro del tubo: apoyado sobre la pared interior.
        shrink = profile.thickness
        y, z = profile.point(d, theta_deg, shrink)
        ny, nz = profile.outward_normal(d, theta_deg, shrink)
        pts.append(cq.Vector(d, y - r * ny, z - r * nz))

    p0, p1 = pts
    axis = p1 - p0

    solid = cq.Solid.makeCylinder(r, axis.Length, p0, axis.normalized())

    return cq.Workplane("XY").newObject([solid])


def create_brachial_tube() -> cq.Workplane:
    # x original 28..113 medido desde el inicio de la carcasa
    return create_tube(
        BRACHIAL_PROFILE,
        BRACHIAL_PROFILE.d0 + 28.0,
        BRACHIAL_PROFILE.d0 + 113.0,
    )


def create_central_tube() -> cq.Workplane:
    return create_tube(
        FOREARM_PROFILE,
        FOREARM_PROFILE.d0 + 20.0,
        FOREARM_PROFILE.d0 + 85.0,
    )


def create_distal_tube() -> cq.Workplane:
    return create_tube(
        FOREARM_PROFILE,
        FOREARM_PROFILE.d0 + 108.0,
        FOREARM_PROFILE.d0 + 168.0,
    )


# ------------------------------------------------------------
# Valvulas / pulsadores: perpendiculares a la cara exterior
# ------------------------------------------------------------


def valve_cylinder(
    profile: ShellProfile,
    d: float,
    theta_deg: float = VALVE_THETA_DEG,
    clearance: float = 0.0,
) -> cq.Workplane:
    """
    Cilindro normal a la superficie, que arranca en la pared interior
    y atraviesa la pared saliendo VALVE_LENGTH hacia el exterior.
    Con `clearance` > 0 sirve como herramienta de corte del agujero.
    """

    shrink = profile.thickness
    y, z = profile.point(d, theta_deg, shrink)
    ny, nz = profile.outward_normal(d, theta_deg, shrink)

    # Como herramienta de corte se extiende 1 mm hacia adentro; como
    # valvula se asienta 0.3 mm por fuera de la pared interior para no
    # interferir con el revestimiento.
    offset = -1.0 if clearance > 0 else 0.3
    base = cq.Vector(d, y + offset * ny, z + offset * nz)
    direction = cq.Vector(0, ny, nz)

    solid = cq.Solid.makeCylinder(
        VALVE_DIAMETER / 2.0 + clearance,
        VALVE_LENGTH - offset,
        base,
        direction,
    )

    return cq.Workplane("XY").newObject([solid])
