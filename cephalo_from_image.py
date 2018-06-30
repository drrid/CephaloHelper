import numpy as np
import cv2
import bonefinder_addon as helper
import imutils


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def prepare_img(path):

    #Read Image from path...
    image = cv2.imread(path)

    #Apply Canny Edge...
    image = imutils.resize(image, height=700)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 10, 40)

    return edged


def find_contour(img):
    _, contours,h = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > 10000:
                print("Contour found...")
                break
    return approx


def find_points(img):
    pts = []
    _, contours,h = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        M = cv2.moments(cnt)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        pts.append([cX, cY])
    return pts


path = 'C://Users//Tarek//Pictures//negato_neopixel2.jpg'
img = prepare_img(path)

cv2.imshow('img1', img)
contour = find_contour(img)
warped = four_point_transform(img, contour.reshape(4, 2))

h, w = warped.shape
cropped = cv2.resize(warped[10:h-10, 10:w-10], (480, 682))
h1, w1 = cropped.shape
ratio = w1/204
pts = find_points(cropped)
for i, p in enumerate(pts):
    cv2.putText(cropped, str(i), (p[0], p[1]), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)
print(len(pts))
angle_test = helper.get_angle(pts[1], pts[0], pts[2])
a = np.array((pts[0][0], pts[0][1]))
b = np.array((pts[1][0], pts[1][1]))
dist = np.linalg.norm(a-b)
print(dist/ratio)
print(angle_test)


cv2.imshow('img', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
