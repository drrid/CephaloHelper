import numpy as np
def get_angle(p0, p1=np.array([0,0]), p2=None):
    ''' compute angle (in degrees) for p0p1p2 corner
    Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return round(abs(np.degrees(angle)))

p1 = [401.91363525390625, 62.323429107666016]
p2 = [211.30540466308594, 259.9956970214844]
p3 = [382.40155029296875, 435.78802490234375]

print(get_angle(p1, p2, p3))