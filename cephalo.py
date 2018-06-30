import cv2
import numpy as np
from imutils import contours


plane = []
points = []


def get_angle(p0, p1=np.array([0,0]), p2=None):
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return round(abs(np.degrees(angle)), 1)


def get_points(path):
    points.clear()
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(im)
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # cnts = cv2.findContours(keypoints, cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)

    # im_with_keypoints, _ = contours.sort_contours(im_with_keypoints)
    keypoints = sorted(keypoints, key=lambda k: [k.pt[0]])
    for i, keypoint in enumerate(keypoints):
        im_with_text = cv2.putText(im,str(i), (int(keypoint.pt[0]), int(keypoint.pt[1])),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, 15)
        points.append([keypoint.pt[0], keypoint.pt[1]])

    # for i in [7, 15, 6]:
        # print(str(keypoints[i].pt[0]) + ', ' + str(keypoints[i].pt[1]))
        # plane.append([keypoints[i].pt[0], keypoints[i].pt[1]])
    # cv2.imshow("Keypoints", im_with_keypoints)
    cv2.imshow("Keypoints", im)
    cv2.waitKey(0)


get_points("blob3.jpg")
print("blob3")
print("SNA: ", get_angle(points[2], points[3], points[1]))
print("SNB: ", get_angle(points[2], points[3], points[0]))
print("ANB: ", get_angle(points[1], points[3], points[0]))


# for i, p in enumerate(points):
#     for i2, p2 in enumerate(points):
#         if (p[0] == p2[0]) and (i != i2):
#             print(p[0])
#         if (p[1] == p2[1]) and (i != i2):
#             print(p[1])

