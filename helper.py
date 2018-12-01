import numpy as np
import math


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
L11_gonion,
L12_articulate,
L13_I1,
L14_I2,
L15_i1,
L16_i2,
L17_M1,
L18_M2,
L19_m1,
L20_m2]
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
    # return np.degrees(angle)

#
# angles = {}
# pts = get_points("ceph2.pts")
#
#
# #Angles usuelles
# angles['SNA'] = get_angle(pts[0], pts[1], pts[4])
# angles['SNB'] = get_angle(pts[0], pts[1], pts[5])
# angles['ANB'] = angles['SNA'] - angles['SNB']
# angles['AC'] = 180 - (get_angle(pts[6], pts[4], pts[1]))
# angles['AF'] = get_angle(pts[3], pts[2], pts[6])
# angles['FMA'] = get_angle_lines(pts[2], pts[3], pts[7], pts[9])
# angles['AXE-Y'] = get_angle_lines(pts[0], pts[8], pts[3], pts[2])
# angles['AG'] = get_angle(pts[7], pts[9], pts[18])
#
# for key, value in angles.items():
#     print(key + ": " + str(value))
