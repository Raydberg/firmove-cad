import cadquery as cq

from .parameters import (
    BRAQUIAL_LENGTH,
    BRAQUIAL_WIDTH_ELBOW,
    BRAQUIAL_HEIGHT_ELBOW,
    BRAQUIAL_WIDTH_PROXIMAL,
    BRAQUIAL_HEIGHT_PROXIMAL,
    SHELL_THICKNESS,
)


def _create_half_oval_shell(
    length: float,
    width_start: float,
    height_start: float,
    width_end: float,
    height_end: float,
    thickness: float,
) -> cq.Workplane:
    """
    Crea una carcasa hueca mediante loft de secciones elipticas
    y elimina la mitad superior para obtener una ortesis tipo canal.
    """

    outer = (
        cq.Workplane("YZ")
        .ellipse(width_start / 2.0, height_start / 2.0)
        .workplane(offset=length)
        .ellipse(width_end / 2.0, height_end / 2.0)
        .loft(combine=True)
    )

    inner = (
        cq.Workplane("YZ")
        .ellipse(
            width_start / 2.0 - thickness,
            height_start / 2.0 - thickness,
        )
        .workplane(offset=length)
        .ellipse(
            width_end / 2.0 - thickness,
            height_end / 2.0 - thickness,
        )
        .loft(combine=True)
    )

    shell = outer.cut(inner)

    max_width = max(width_start, width_end)
    max_height = max(height_start, height_end)

    # Elimina la mitad superior (+Z), dejando la carcasa abierta.
    opening_cut = (
        cq.Workplane("XY")
        .box(
            length + 20.0,
            max_width + 20.0,
            max_height,
            centered=(True, True, False),
        )
        .translate((length / 2.0, 0, 0))
    )

    shell = shell.cut(opening_cut)

    return shell


def _add_ventilation_slots(
    shell: cq.Workplane,
    length: float,
    max_height: float,
) -> cq.Workplane:

    slot_length = 17.0
    slot_width = 5.0

    positions = (
        0.22,
        0.38,
        0.56,
        0.74,
    )

    result = shell

    for fraction in positions:
        cutter = (
            cq.Workplane("XY")
            .box(
                slot_length,
                slot_width,
                max_height + 12.0,
                centered=(True, True, True),
            )
            .translate(
                (
                    length * fraction,
                    0,
                    -max_height * 0.35,
                )
            )
        )

        result = result.cut(cutter)

    return result


def create_brachial_module() -> cq.Workplane:

    shell = _create_half_oval_shell(
        length=BRAQUIAL_LENGTH,
        width_start=BRAQUIAL_WIDTH_ELBOW,
        height_start=BRAQUIAL_HEIGHT_ELBOW,
        width_end=BRAQUIAL_WIDTH_PROXIMAL,
        height_end=BRAQUIAL_HEIGHT_PROXIMAL,
        thickness=SHELL_THICKNESS,
    )

    shell = _add_ventilation_slots(
        shell,
        BRAQUIAL_LENGTH,
        max(
            BRAQUIAL_HEIGHT_ELBOW,
            BRAQUIAL_HEIGHT_PROXIMAL,
        ),
    )

    return shell