from pathlib import Path

import cadquery as cq

from src.assembly import create_firmove_assembly
from src.brachial_module import create_brachial_module
from src.forearm_module import create_forearm_module
from src.hinge import create_hinge


ROOT = Path(__file__).resolve().parent

OUTPUT_DIR = ROOT / "output"
PARTS_DIR = OUTPUT_DIR / "parts"

OUTPUT_DIR.mkdir(exist_ok=True)
PARTS_DIR.mkdir(exist_ok=True)


def export_part(
    part: cq.Workplane,
    filename: str,
) -> None:

    path = PARTS_DIR / filename

    cq.exporters.export(
        part,
        str(path),
    )

    print(
        f"[OK] {path.relative_to(ROOT)} "
        f"({path.stat().st_size / 1024:.1f} KB)"
    )


def main() -> None:

    print("=" * 60)
    print("FIRMOVE - Generador CAD conceptual")
    print("=" * 60)

    # --------------------------------------------------
    # Exportar piezas principales
    # --------------------------------------------------

    print("\nGenerando modulo braquial...")

    brachial = create_brachial_module()

    export_part(
        brachial,
        "MODULO_BRAQUIAL_01.step",
    )

    print("\nGenerando modulo antebraquial...")

    forearm = create_forearm_module()

    export_part(
        forearm,
        "MODULO_ANTEBRAQUIAL_02.step",
    )

    print("\nGenerando bisagra...")

    hinge = create_hinge()

    export_part(
        hinge,
        "BISAGRA_VISUAL_03.step",
    )

    # --------------------------------------------------
    # Ensamblaje completo
    # --------------------------------------------------

    print("\nConstruyendo ensamblaje FIRMOVE...")

    assembly = create_firmove_assembly()

    output_file = OUTPUT_DIR / "FIRMOVE.step"

    assembly.export(
        str(output_file),
        unit="MM",
    )

    size_kb = output_file.stat().st_size / 1024

    print(
        f"\n[OK] {output_file.relative_to(ROOT)} "
        f"({size_kb:.1f} KB)"
    )

    print("\nModelo generado correctamente.")

    print("\nArchivos:")
    print("  output/FIRMOVE.step")
    print("  output/parts/MODULO_BRAQUIAL_01.step")
    print("  output/parts/MODULO_ANTEBRAQUIAL_02.step")
    print("  output/parts/BISAGRA_VISUAL_03.step")


if __name__ == "__main__":
    main()