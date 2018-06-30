import numpy as np
import cv2
import bonefinder_addon as helper


img = cv2.imread('C://Users//Tarek//Pictures//detect_skew.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

pts = []
pts_skew = []

gray2 = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray2, 75, 200)
cv2.imshow('img_edged',edged)
_, contours,h = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    area = cv2.contourArea(cnt)

    if area > 7 and area < 10:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        pts.append([cX, cY])
        cv2.putText(img, str(cX) + '/' +str(cY) + '--' + str(area), (cX + 1, cY + 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # print(cX, cY)
        cv2.drawContours(img, [cnt], 0, 255, -1)

    if area > 20 and area < 200:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        pts_skew.append([cX, cY])
        cv2.putText(img, str(cX) + '/' + str(cY) + '--' + str(area), (cX + 1, cY + 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        print(cX, cY)
        cv2.drawContours(img, [cnt], 0, (0,255,180), -1)


pts1 = np.float32([pts_skew[0], pts_skew[1], pts_skew[4], pts_skew[3]])
pts2 = np.float32([[0, 0], [548, 0], [0, 953], [548, 953]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (548, 953))

cv2.imshow('img_warped',result)


########################################################################################################
gray4 = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

pts33 = []
pts_skew = []

gray5 = cv2.GaussianBlur(gray4, (5, 5), 0)
edged4 = cv2.Canny(gray5, 75, 200)
cv2.imshow('img_edged',edged4)
_, contours2,h = cv2.findContours(edged4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in contours2:
    area = cv2.contourArea(cnt)
    print(str(area) + "------")

    if area < 90:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        pts33.append([cX, cY])
        cv2.putText(img, str(cX) + '/' + str(cY) + '--' + str(area), (cX + 1, cY + 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # print(cX, cY)
        cv2.drawContours(result, [cnt], 0, (0,255,180), -1)
########################################################################################################
# print(pts)
print(helper.get_angle(pts33[0], pts33[1], pts33[2]))
print(helper.get_angle(pts33[1], pts33[0], pts33[2]))
print(helper.get_angle(pts33[1], pts33[2], pts33[0]))

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


