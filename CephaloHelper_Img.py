import numpy as np
import cv2
import helper as helper
import imutils

# TODO: Extract 'ENA, ENP' and Calculate angles.

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
    image = imutils.resize(image, height=1200)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 15,50)

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

    warped = four_point_transform(img, approx.reshape(4, 2))
    h, w = warped.shape
    cropped = cv2.resize(warped[20:h - 20, 20:w - 20], (800, 1136))
    h1, w1 = cropped.shape
    ratio = w1 / 204

    return cropped


def find_points(img):
    pts = []
    _, contours,h = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        M = cv2.moments(cnt)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        pts.append([cX, cY])
    return pts


def sort_points(pts):
    dict = {}

    #Extract 'S, Po, Ar, Go'...
    ordered_y = sorted(pts, key= lambda pt: pt[1])[0:4]
    ordered_x = sorted(ordered_y, key=lambda pt: pt[0])
    pts_new = [pt for pt in pts if pt not in ordered_x]
    dict.update({'S': ordered_x[3], 'Po': ordered_x[2], 'Ar': ordered_x[1], 'Go': ordered_x[0]})

    #Extraction des molaires ;)...
    ordered_y = sorted(pts_new, key= lambda pt: pt[1])[4:]
    ordered_y_m = sorted(pts_new, key=lambda pt: pt[1])[0:4]
    ordered_x_m = sorted(ordered_y_m , key=lambda pt: pt[0])
    dict.update({'M1': ordered_x_m[2], 'M2': ordered_x_m[3], 'm_1': ordered_x_m[1], 'm_2': ordered_x_m[0]})

    #Extract 'Me, Gn, Na, Or, I1, I2, A, i_1'...
    ordered_x = sorted(ordered_y, key=lambda pt: pt[0])
    dict.update({'Me': ordered_x[0], 'Gn': ordered_x[1], 'Na': ordered_x[-1], 'i_1': ordered_x[-5],
                 'Or': ordered_x[-2], 'I2': ordered_x[-3], 'A': ordered_x[-4], 'I1': ordered_x[-6]})

    #Extract 'B, Pog, i_2'...
    pts_remain = [ordered_x[2], ordered_x[3], ordered_x[4]]
    ordered_y = sorted(pts_remain, key=lambda pt: pt[1])[1:3]
    i2 = sorted(pts_remain, key=lambda pt: pt[1])[0]
    ordered_x = sorted(ordered_y, key=lambda pt: pt[0])
    dict.update({'B': ordered_x[1], 'Pog': ordered_x[0], 'i_2': i2})

    return dict



path = 'pts.jpg'
img = prepare_img(path)
cv2.imshow('img1', img)

contour = find_contour(img)
pts = find_points(contour)

dict = sort_points(pts)

for pt, coord in dict.items():
    cv2.putText(contour, pt, (coord[0], coord[1]), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)

cv2.imshow('img', contour)
cv2.waitKey(0)
cv2.destroyAllWindows()
