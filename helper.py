import numpy as np
import math

SNA_dsc = "(83° ±3°) Maxillaire normale par rapport à la base du crâne"
SNA_dsc_plus = "(83° ±3°) Maxillaire en avant par rapport à la base du crâne"
SNA_dsc_minus = "(83° ±3°) Maxillaire en retrait par rapport à la base du crâne"

SNB_dsc = "(80° ±3°) Mandibule normale par rapport à la base du crâne"
SNB_dsc_plus = "(80° ±3°) Mandibule en avant par rapport à la base du crâne"
SNB_dsc_minus = "(80° ±3°) Mandibule en retrait par rapport à la base du crâne"

ANB_dsc = "(3° ±1°) Mandibule normale par rapport au maxillaire, Classe I squelettique"
ANB_dsc_plus = "(3° ±1°) Mandibule en retrait par rapport au maxillaire, Classe II squelettique"
ANB_dsc_minus = "(3° ±1°) Mandibule en avant par rapport au maxillaire, Classe III squelettique"

SND_dsc = "(76°) Normogénie"
SND_dsc_plus = "(76°) Progénie"
SND_dsc_minus = "(76°) Rétrogénie"

AC_dsc = "(6° ±5°) Type rectiligne"
AC_dsc_plus = "(6° ±5°) Type convexe"
AC_dsc_minus = "(6° ±5°) Type concave"

E_SUP_dsc = "(45.5% ±2%) Etage supérieure normal"
E_SUP_dsc_plus = "(45.5% ±2%) Etage supérieure augmenté"
E_SUP_dsc_minus = "(45.5% ±2%) Etage supérieure diminué"

E_INF_dsc = "(54.5% ±2%) Etage inférieure normal"
E_INF_dsc_plus = "(54.5% ±2%) Etage inférieure augmenté"
E_INF_dsc_minus = "(54.5% ±2%) Etage inférieure diminué"

AF_dsc = "(90° ±3°) Normoposition du menton"
AF_dsc_plus = "(90° ±3°) Protrusion du menton"
AF_dsc_minus = "(90° ±3°) Rétrusion du menton"

AoBo_dsc = "(1mm ±2mm) Les maxillaires ont des rapports harmonieux"
AoBo_dsc_plus = "(1mm ±2mm) Classe II squelettique"
AoBo_dsc_minus = "(1mm ±2mm) Classe III squelettique"

FMA_dsc = "(27° ±4°) Croissance mandibulaire moyenne"
FMA_dsc_plus = "(27° ±4°) Croissance mandibulaire à tendance verticale"
FMA_dsc_minus = "(27° ±4°) Croissance mandibulaire à tendance horizontale"

AXE_Y_dsc = "(59° ±3°) Croissance faciale moyenne"
AXE_Y_dsc_plus = "(59° ±3°) Croissance faciale à tendance verticale"
AXE_Y_dsc_minus = "(59° ±3°) Croissance faciale à tendance horizontale"

AG_dsc = "(128° ±6°) Normodivergence"
AG_dsc_plus = "(128° ±6°) Hyperdivergence"
AG_dsc_minus = "(128° ±6°) Hypodivergence"

I_F_dsc = "(107° ±3°) Normoalvéolie Supérieure"
I_F_dsc_plus = "(107° ±3°) Proalvéolie supérieure"
I_F_dsc_minus = "(107° ±3°) Rétroalvéolie supérieure"

I_M_dsc = "(90° ±3°) Normoalvéolie inférieure"
I_M_dsc_plus = "(90° ±3°) Proalvéolie inférieure"
I_M_dsc_minus = "(90° ±3°) Rétroalvéolie inférieure"

I_I_dsc = "(135° ±5°) Normoalvéolie"
I_I_dsc_plus = "(135° ±5°) Rétrusion du bloc incisif"
I_I_dsc_minus = "(135° ±5°) Protrusion du bloc incisif"

ALPHA_dsc = "(90° ±3°) Normoposition de la molaire supérieure"
ALPHA_dsc_plus = "(90° ±3°) Mésioversion de la molaire supérieure"
ALPHA_dsc_minus = "(90° ±3°) Distoversion de la molaire supérieure"

BETA_dsc = "(100° ±3°) Normoposition de la molaire inférieure"
BETA_dsc_plus = "(100° ±3°) Mésioversion de la molaire inférieure"
BETA_dsc_minus = "(100° ±3°) Distoversion de la molaire inférieure"

'''
[L0_sella,
L1_nasion,
L2_porion,
L3_orbitale,
L4_ENP,
L5_ENA,
L6_point_A,
L7_point_B,
L8_pogonion,
L9_menton,
L10_gnathion,
L11_symphyse
L12_gonion,
L13_articulate,
L14_I1,
L15_I2,
L16_i1,
L17_i2,
L18_M1,
L19_M2,
L20_m1,
L21_m2]
'''


def dot(v, w):
    x, y = v
    X, Y = w
    return x * X + y * Y
def length(v):
    x, y = v
    return math.sqrt(x * x + y * y)
def vector(b, e):
    x, y = b
    X, Y = e
    return (X - x, Y - y)
def unit(v):
    x, y = v
    mag = length(v)
    return (x / mag, y / mag)
def distance(p0, p1):
    return length(vector(p0, p1))
def scale(v, sc):
    x, y = v
    return (x * sc, y * sc)
def add(v, w):
    x, y = v
    X, Y = w
    return (x + X, y + Y)

def aobo_verify(pnt_A, pnt_B, POP, POA, clb1, clb2):
    clb1 = np.array(clb1)
    clb2 = np.array(clb2)
    clb = np.linalg.norm(clb1 - clb2)

    pnt_Ao = np.array(pnt2line(pnt_A, POA, POP))
    pnt_Bo = np.array(pnt2line(pnt_B, POA, POP))

    if (pnt_Ao[0] < pnt_Bo[0]):
        AoBo = np.linalg.norm(pnt_Ao - pnt_Bo)
        AoBo = round(AoBo*10/clb)*-1
    else:
        AoBo = np.linalg.norm(pnt_Ao - pnt_Bo)
        AoBo = round(AoBo*10/clb)
    return (AoBo)

def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    nearest = [float(nearest[0]), float(nearest[1])]
    return (nearest)


def rapport_etage(pnt, start, end):

    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)


    ena_prime = [float(nearest[0]), float(nearest[1])]

    na = np.array(start)
    me = np.array(end)
    ena = np.array(ena_prime)

    dist_total = np.linalg.norm(na-me)
    dist_sup = np.linalg.norm(na - ena)
    dist_inf = np.linalg.norm(ena - me)

    es = round(dist_sup*100/dist_total, 2)
    ei = round(dist_inf * 100 / dist_total, 2)

    return(es, ei)


def get_points(path):
    points = []
    with open(path, 'r') as pts_file:
        for line in pts_file:
            if line[0].isdigit():
                pt = line.replace('\n', '')
                x, y = pt.split(" ")
                points.append([float(x), float(y)])
    return(points)


def get_angle(p0, p1=np.array([0,0]), p2=None):
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return round(abs(np.degrees(angle)), 1)


def get_angle_lines(p0, p1, p2, p3):

    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p3)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return round(abs(np.degrees(angle)), 1)


