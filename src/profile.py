"""
Perfil geometrico de una carcasa (loft reglado entre dos elipses).

Al ser un loft reglado entre dos secciones elipticas, la seccion en
cualquier distancia d es una elipse cuyos semiejes varian linealmente.
Esto permite ubicar con exactitud pads, tubos, valvulas, correas y
barras de la bisagra sobre la superficie real de la carcasa.

Marco local: +X sale del pivote; el ancho va en Y y la altura en Z.
"""

import math
from dataclasses import dataclass

from .parameters import (
    BRAQUIAL_LENGTH,
    BRAQUIAL_WIDTH_ELBOW,
    BRAQUIAL_HEIGHT_ELBOW,
    BRAQUIAL_WIDTH_PROXIMAL,
    BRAQUIAL_HEIGHT_PROXIMAL,
    FOREARM_LENGTH,
    FOREARM_WIDTH_ELBOW,
    FOREARM_HEIGHT_ELBOW,
    FOREARM_WIDTH_WRIST,
    FOREARM_HEIGHT_WRIST,
    SHELL_THICKNESS,
    ELBOW_SETBACK,
)


@dataclass(frozen=True)
class ShellProfile:
    d0: float  # distancia pivote -> inicio de la carcasa
    length: float
    width0: float
    height0: float
    width1: float
    height1: float
    thickness: float

    @property
    def d1(self) -> float:
        return self.d0 + self.length

    def _lerp(self, d: float, v0: float, v1: float) -> float:
        u = (d - self.d0) / self.length
        return v0 + (v1 - v0) * u

    def half_width(self, d: float, shrink: float = 0.0) -> float:
        """Semieje en Y de la superficie exterior (menos `shrink`)."""
        return self._lerp(d, self.width0, self.width1) / 2.0 - shrink

    def half_height(self, d: float, shrink: float = 0.0) -> float:
        """Semieje en Z de la superficie exterior (menos `shrink`)."""
        return self._lerp(d, self.height0, self.height1) / 2.0 - shrink

    def point(self, d: float, theta_deg: float, shrink: float = 0.0):
        """
        Punto (y, z) de la elipse a distancia d. theta se mide desde +Y
        hacia -Z. Un theta constante recorre una recta sobre la
        superficie del loft reglado.
        """
        th = math.radians(theta_deg)
        a = self.half_width(d, shrink)
        b = self.half_height(d, shrink)
        return a * math.cos(th), -b * math.sin(th)

    def outward_normal(self, d: float, theta_deg: float, shrink: float = 0.0):
        """Normal exterior unitaria (ny, nz) de la elipse en ese punto."""
        a = self.half_width(d, shrink)
        b = self.half_height(d, shrink)
        y, z = self.point(d, theta_deg, shrink)
        ny, nz = y / a**2, z / b**2
        n = math.hypot(ny, nz)
        return ny / n, nz / n

    def bottom_z(self, d: float, y: float = 0.0, shrink: float = 0.0) -> float:
        """Cota Z de la superficie (parte inferior) en (d, y)."""
        a = self.half_width(d, shrink)
        b = self.half_height(d, shrink)
        return -b * math.sqrt(max(0.0, 1.0 - (y / a) ** 2))


BRACHIAL_PROFILE = ShellProfile(
    d0=ELBOW_SETBACK,
    length=BRAQUIAL_LENGTH,
    width0=BRAQUIAL_WIDTH_ELBOW,
    height0=BRAQUIAL_HEIGHT_ELBOW,
    width1=BRAQUIAL_WIDTH_PROXIMAL,
    height1=BRAQUIAL_HEIGHT_PROXIMAL,
    thickness=SHELL_THICKNESS,
)

FOREARM_PROFILE = ShellProfile(
    d0=ELBOW_SETBACK,
    length=FOREARM_LENGTH,
    width0=FOREARM_WIDTH_ELBOW,
    height0=FOREARM_HEIGHT_ELBOW,
    width1=FOREARM_WIDTH_WRIST,
    height1=FOREARM_HEIGHT_WRIST,
    thickness=SHELL_THICKNESS,
)
