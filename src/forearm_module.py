import cadquery as cq

from .parameters import (
    FOREARM_LENGTH,
    FOREARM_WIDTH_ELBOW,
    FOREARM_HEIGHT_ELBOW,
    FOREARM_WIDTH_WRIST,
    FOREARM_HEIGHT_WRIST,
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

    return shell.cut(opening_cut)


def _add_ventilation_slots(
    shell: cq.Workplane,
    length: float,
    max_height: float,
) -> cq.Workplane:

    result = shell

    positions = (
        0.18,
        0.32,
        0.48,
        0.64,
        0.80,
    )

    for fraction in positions:
        cutter = (
            cq.Workplane("XY")
            .box(
                18.0,
                4.5,
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


def create_forearm_module() -> cq.Workplane:

    shell = _create_half_oval_shell(
        length=FOREARM_LENGTH,
        width_start=FOREARM_WIDTH_ELBOW,
        height_start=FOREARM_HEIGHT_ELBOW,
        width_end=FOREARM_WIDTH_WRIST,
        height_end=FOREARM_HEIGHT_WRIST,
        thickness=SHELL_THICKNESS,
    )

    shell = _add_ventilation_slots(
        shell,
        FOREARM_LENGTH,
        max(
            FOREARM_HEIGHT_ELBOW,
            FOREARM_HEIGHT_WRIST,
        ),
    )

    return shell