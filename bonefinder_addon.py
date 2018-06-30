import numpy as np

'''
[L1_sella,
L2_nasion,
L3_orbitale,
L4_porion,
L5_subspinale_A,
L6_supramentale_B,
L7_pogonion,
L8_menton,
L9_gnathion,
L10_gonion,
L11_lower_incisal_incision,
L12_upper_incisal_incision,
L13_upper_lip,
L14_lower_lip,
L15_subnasale,
L16_soft_tissue_pogonion,
L17_posterior_nasal_spine,
L18_anterior_nasal_spine,
L19_articulate]
'''


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
