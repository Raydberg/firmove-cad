# ============================================================
# FIRMOVE - PARAMETROS CONCEPTUALES
# Unidades: milimetros
#
# Convenciones del modelo:
#   - Eje de flexion del codo: eje Z, pasando por el origen (pivote).
#   - Cada modulo se define en su marco local: +X sale del pivote
#     hacia el extremo libre del modulo.
#   - "d" = distancia medida desde el pivote a lo largo del eje
#     local del modulo.
#   - Las carcasas son canales abiertos hacia +Z; la cara exterior
#     (lateral) esta en -Z y es la que se ve en las referencias.
#   - theta: posicion angular sobre la seccion eliptica, medida desde
#     +Y hacia -Z (90 = centro de la cara exterior).
# ============================================================

# -------------------------
# Modulo braquial
# -------------------------

BRAQUIAL_LENGTH = 150.0

# Seccion cerca del codo
BRAQUIAL_WIDTH_ELBOW = 72.0
BRAQUIAL_HEIGHT_ELBOW = 50.0

# Seccion proximal
BRAQUIAL_WIDTH_PROXIMAL = 82.0
BRAQUIAL_HEIGHT_PROXIMAL = 60.0


# -------------------------
# Modulo antebraquial
# -------------------------

FOREARM_LENGTH = 190.0

# Cerca del codo
FOREARM_WIDTH_ELBOW = 72.0
FOREARM_HEIGHT_ELBOW = 48.0

# Cerca de la muneca
FOREARM_WIDTH_WRIST = 58.0
FOREARM_HEIGHT_WRIST = 38.0


# -------------------------
# Carcasas
# -------------------------

SHELL_THICKNESS = 4.0

# Distancia entre el pivote y el inicio de cada carcasa. Evita que las
# carcasas se crucen en el interior del angulo del codo (minimo
# geometrico ~ 19 mm para 125 grados y 36 mm de semiancho) y deja
# espacio para la bisagra.
ELBOW_SETBACK = 22.0

# La abertura se corta por encima del ecuador de la elipse, de modo
# que la carcasa envuelve mas de media seccion (como una ortesis real).
SHELL_OPENING_Z = 6.0

# Redondeo del borde de la abertura
SHELL_RIM_FILLET = 1.2

# Redondeo en planta de los extremos de cada carcasa
SHELL_END_RADIUS_ELBOW = 8.0
SHELL_END_RADIUS_FREE = 14.0


# -------------------------
# Posicion general
# -------------------------

# Angulo interior conceptual del codo
ELBOW_ANGLE = 125.0

# Como el brazo se extiende hacia -X,
# el antebrazo se rota:
FOREARM_ROTATION_DEG = 180.0 - ELBOW_ANGLE


# -------------------------
# Ventilacion (distancias d desde el pivote)
# -------------------------

SLOT_LENGTH = 10.0
SLOT_WIDTH = 4.0

BRAQUIAL_SLOT_POSITIONS = (100.0, 112.0, 124.0, 136.0)
FOREARM_SLOT_POSITIONS = (97.0, 109.0, 121.0)


# -------------------------
# Bisagra
# -------------------------

HINGE_DIAMETER = 60.0
HINGE_THICKNESS = 6.0

HINGE_AXIS_DIAMETER = 8.0

# La bisagra coincide con el eje de flexion (pivote en el origen).
HINGE_SIDE_OFFSET = 0.0

# Cota Z de la cara exterior (inferior) del disco. Las demas capas
# (barras, disco) se apilan hacia -Z, por fuera de las carcasas:
#   carcasa antebraquial -> barra antebraquial -> barra braquial -> disco
HINGE_Z = -35.0

HINGE_BAR_THICKNESS = 2.5
HINGE_BAR_LENGTH = 62.0
HINGE_BAR_WIDTH = 14.0

HINGE_HUB_DIAMETER = 14.0
HINGE_HUB_HEIGHT = 3.0

HINGE_REF_RADIUS = 26.0
HINGE_REF_HOLE_DIAMETER = 1.2

STOP_PIN_DIAMETER = 2.0
STOP_PIN_HEIGHT = 10.0


# -------------------------
# Correas (distancias d desde el pivote)
# -------------------------

STRAP_WIDTH = 18.0
STRAP_THICKNESS = 3.0
STRAP_CLEARANCE = 0.3

BUCKLE_LENGTH = 14.0
BUCKLE_WIDTH = 22.0
BUCKLE_THICKNESS = 3.0

# Separadas de la barra de la bisagra y de las ranuras de ventilacion.
BRAQUIAL_STRAP_POSITIONS = (80.0, 152.0)
FOREARM_STRAP_POSITIONS = (76.0, 138.0, 196.0)


# -------------------------
# Sistema neumatico
# -------------------------

AIR_CHAMBER_THICKNESS = 8.0

TUBE_DIAMETER = 3.0

VALVE_DIAMETER = 7.0
VALVE_LENGTH = 10.0
VALVE_HOLE_CLEARANCE = 0.4

LINER_THICKNESS = 2.0

# Posicion angular de tubos (cara interior) y valvulas (cara exterior)
TUBE_THETA_DEG = 20.0
VALVE_THETA_DEG = 72.0

# Distancias d desde el pivote
BRAQUIAL_VALVE_D = 116.0
FOREARM_CENTRAL_VALVE_D = 108.0
FOREARM_DISTAL_VALVE_D = 165.0
